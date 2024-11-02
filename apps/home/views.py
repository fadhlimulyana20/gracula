from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
def index(request):
    return render(request, 'home/index.html')


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        # Static data for testing
        context = {
            'name': 'John Doe',
            'user_id': 12345
        }
        
        # Render the HTML template
        html_content = render_to_string('emails/email_template.html', context)
        plain_message = strip_tags(html_content)
        
        # Set up the email details
        subject = 'Test Email'
        from_email = 'your_email@example.com'
        to_email = 'recipient@example.com'
        
        # # Create the email message
        # email = EmailMultiAlternatives(subject, '', from_email, [to_email])
        # email.attach_alternative(html_content, "text/html")
        
        try:
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_content)
            return Response({"message": "Email sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)