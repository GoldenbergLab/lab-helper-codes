# How to add a new user to our AWS server

1. Navigate to **IAM** (Identity and Access Management)
2. If the user already exists (and is inactive), click on their name. If the user is not already existent, click **Add users** and enter their information.
  a. New users: create a username and **enable console access** so the user can log into the interface. Make sure to click **Custom password** and set a dummy password that the user must change upon next login by checking **Users must create a new password at next sign-in.** Inform your user of their new dummy password and send them their login link.
3. Assign the user to a user group, which will give them the appropriate permissions. Our user groups are:
  - **Administrators:** for those who need full permissions 
  - **Lab members:** for those who are a part of our lab and will run experiments
  - **Guests:** for those who are running 1-2 specific experiments and only need access to certain buckets or services (not all)

