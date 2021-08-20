# Fernetazo

Encrypt/Decrypt text

## How to use it

```python
python3 fernetazo.py [--encrypt | --decrypt ]
```

Always one (and only one) of the arguments must be included.


## Encrypt

* Create a txt file with named `encrypt.txt`.
* Run the script with the `--encrypt` argument.
* Set the password for your encryption.
* Store the token you get.

## Decrypt

* Run the script with the `--decrypt` argument.
* Use the password and token when file was encrypted.
* You will get a file named `decrypt.txt` with the message previously encrypted.

## Salt

This method is based on the use of something called `salt` to generate the encryption/decryption key of the Fernet element. To always get the same output with the password used, the salt should be always the same. For that reason, it is store as an environmental variable and you must always keep a safe back-up. Of course not the safest approach, but this is only a practice script not intended to be used in Production.
