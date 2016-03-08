import smtpd
import asyncore
import base64

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        
        text = data.split('\n\n')
        d = {'header': text[0], 'body': base64.b64decode(text[1])}
        print "{header}\n\n\n{body}".format(**d)
        print "\n\n====================END OF MESSAGE====================\n\n"
        return

server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
