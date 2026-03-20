## Сгенерировать ключи

```
mkdir certs
cd certs
openssl genrsa -out private_jwt.pem 2048
openssl rsa -in private_jwt.pem -pubout -out public_jwt.pem
```