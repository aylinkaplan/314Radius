# Requirements

* Python (3.8.2)
* Flask (1.1.2)


# Installation
```
pip install -r requirements.txt 
```

#Run and Test Code

```
python application.py 
python test_application.py
```

Example with curl:
```
curl --header "Content-Type: application/json" --request POST --data '["John", "Smith", "1985-12-04", "Back to the Future" ]' http://0.0.0.0:8080/list 
curl --header "Content-Type: application/json" --request POST --data '{"first_name":"John", "last_name":"Smith", "d_o_b":"1985-12-04", "favorite_film":"Back to the Future" }' http://0.0.0.0:8080/json 
```

#Deployment to AWS Beanstalk

```
eb init -p python-3.6 flask-tutorial --region eu-central-1
eb create flask-env
eb open
```

#Self-signed certificate
```
eb ssh
openssl genrsa 2048 > privatekey.pem
openssl req -new -key privatekey.pem -out csr.pem
openssl x509 -req -days 365 -in csr.pem -signkey privatekey.pem -out public.crt
aws iam upload-server-certificate --server-certificate-name elastic-beanstalk --certificate-body file://public.crt --private-key file://privatekey.pem
```

#Configure EBS to terminate HTTPS
For Classic Load Balancer:

    a.Choose Add listener.

    b.In the Classic Load Balancer listener dialog box, configure the following settings:
    
        For Listener port, type the incoming traffic port, typically 443.
        For Listener protocol, choose HTTPS.
        For Instance port, type 80.
        For Instance protocol, choose HTTP.
        For SSL certificate, choose your certificate.

    c.Choose Add.

    d.Choose Apply.

#Application AWS URL
https://flask-env-v6.eba-gxpkbtme.eu-central-1.elasticbeanstalk.com/
