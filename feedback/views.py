from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from analysis.models import AnalysisResult
from feedback.models import FeedbackEntry
from feedback.services.phi import get_feedback_response
import logging

logger = logging.getLogger(__name__)

@login_required
def feedback_view(request):
    try:
        latest_analysis = AnalysisResult.objects.filter(user=request.user).order_by('-timestamp').first()

        if not latest_analysis:
            return render(request, 'feedback/no_analysis.html')

        if request.method == 'POST':
            # Build a comprehensive prompt with all relevant academic data
            prompt = (
                f"The student's GPA is {latest_analysis.gpa}, "
                f"with {latest_analysis.failing_units} failing units "
                f"out of {latest_analysis.num_units} total. "
                f"Their classification is '{latest_analysis.classification}'. "
                f"Please give actionable, motivating advice."
            )

            try:
                ai_response = get_feedback_response(prompt)
                
                # Create feedback entry
                entry = FeedbackEntry.objects.create(
                    user=request.user,
                    input_summary=prompt,
                    response=ai_response,
                )
                
                messages.success(request, "Feedback generated successfully!")
                return redirect('feedback-view')  # Reloads with new data
                
            except Exception as e:
                logger.error(f"Error generating feedback: {str(e)}")
                messages.error(request, "Sorry, we couldn't generate feedback at this time. Please try again later.")
                return redirect('feedback-view')

        # Get latest feedback for display
        latest_feedback = FeedbackEntry.objects.filter(user=request.user).order_by('-created_at').first()

        return render(request, 'feedback/view.html', {
            'feedback': latest_feedback,
            'analysis': latest_analysis,
        })
        
    except Exception as e:
        logger.error(f"Error in feedback view: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again later.")
        logger.info("Attempting to redirect to home from feedback_view error handler.")
        try:
            response = redirect('home')
            logger.info("Redirect to home prepared successfully from feedback_view.")
            return response
        except Exception as redirect_e:
            logger.error(f"CRITICAL: Failed to redirect to home from feedback_view error handler: {str(redirect_e)}")
            from django.http import HttpResponseServerError
            return HttpResponseServerError("A critical error occurred, and we could not redirect you. Please contact support.")
