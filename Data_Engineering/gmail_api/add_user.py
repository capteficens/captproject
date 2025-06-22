from auth import authenticate_user_interactively

if __name__ == "__main__":
    creds, email = authenticate_user_interactively()
    print(f"Successfully added: {email}")