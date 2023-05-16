# How to manage users on our AWS server

## Creating a new user or reactivating a current user
1. Navigate to **IAM** (Identity and Access Management)
2. If the user already exists (and is inactive), click on their name. If the user is not already existent, click **Add users** and enter their information.
  - **New users:** create a username and **enable console access** so the user can log into the interface. Make sure to click **Custom password** and set a dummy password that the user must change upon next login by checking **Users must create a new password at next sign-in.** Inform your user of their new dummy password and send them their login link.
  - **Current users:** make sure that they are assigned to a user group. If they need help logging in, follow the steps outlined for "new users" (enable console access, create a dummy password, make sure they must change the dummy password when they log in).
3. Assign the user to a user group, which will give them the appropriate permissions. User group admin and lab members have automatic policies associated with their accounts. Guests do not and you will need to manually assign the policy. Our user groups are:
  - **Administrators:** for those who need full permissions 
  - **Lab members:** for those who are a part of our lab and will run experiments
  - **Guests:** for those who are running 1-2 specific experiments and only need access to certain buckets or services (not all). 

