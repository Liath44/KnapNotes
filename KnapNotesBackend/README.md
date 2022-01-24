tokeny gości  
token użytkownika
rejestracja i logowanie

na razie olać fancy edycję notatek

monitorowanie pracy systemu (np. żeby poinformować użytkownika o nowych komputerach, które łączyły się z jego kontem)
NIE XDDDDDDDDDDDDDDDDDDDDDDDDDD


dodać opóźnienie podczas logowania


api
 - zarejestruj
 - zaloguj
 - generuj cookie gościnne
 - autentykuj token
 - udostępnij notatkę (weryfikacja czy samemu sobie nie udostępniamy)
 - zapisz notatkę


baza danych
 - użytkownicy, hasła hashowane
 - aktualne tokeny/cookiesy wraz z użytkownikami i czasem terminacji
 - id_notatki, notatki, użytkownik, czy_zaszyfrowana, czy_publiczna
 - pary kluczy notatek, id_notatki, hasło do notatki (shashowane)
 - 3 ostatnie zalogowania na danego użytkownika - jeśli wszystkie 3 na przestrzeni X minut to lockout
   - id_użytkownika, 3 date_timey

DB Auth:
knadmin
VKiM46nmjYENoemvf8ku.















liath@Magi:~$ sudo mysql_secure_installation

Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No: yes

There are three levels of password validation policy:

LOW    Length >= 8
MEDIUM Length >= 8, numeric, mixed case, and special characters
STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file

Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 1
Please set the password for root here.

New password: 

Re-enter new password: 

Estimated strength of the password: 100 
Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) : y
By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
Success.


Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
Success.

By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.


Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
 - Dropping test database...
Success.

 - Removing privileges on test database...
Success.

Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
Success.

All done! 