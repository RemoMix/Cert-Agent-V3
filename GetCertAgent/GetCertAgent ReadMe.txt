GetCertAgent
	Responsibility
	•	Ensure Outlook is running and accessible.
	•	Scan inbox for new emails received from fdesk@aldahlia.com.
	•	Filter emails whose subject contains certificate keywords (CERT, CER) (case-insensitive).
	•	Download attached PDF files.
	Input
	•	No external input. Operates directly on Outlook inbox.
	Output
	•	PDF files downloaded from matching emails.
	•	Saved to Cert Agent V3/Cert_Inbox.
	•	Saved as “original filename”.
	Does NOT
	•	Parse PDF content.
	•	Extract any data.
	•	Make any business decision.
	Failure behavior
	•	If Outlook is not accessible or no matching emails found → exit without error.
