def create_user(db, user_data):
    """
    Stores user data directly in Firestore with a sequential user ID (starting from 1000) 
    and returns the generated user ID.

    :param db: Firestore client instance
    :param user_data: Dictionary containing user information
    :return: Dictionary with the new user ID or an error message
    """
    print("Starting direct user creation process...")

    try:
        # Step 1: Generate a unique user ID based on document count + 1000
        print("Attempting to fetch user count from Firestore...")
        
        # Fetch all documents, limit to 1 if you just want to check accessibility
        docs = db.collection("users").get()
        user_count = len(docs)  # Count documents directly
        
        print(f"Successfully retrieved user count: {user_count} users found.")

        # Generate the next user ID (starting from 1000)
        next_user_id = 1000 + user_count
        user_id = str(next_user_id)
        print(f"Generated user ID: {user_id}")

        # Step 2: Store user data in Firestore
        print(f"Storing user data in Firestore with ID: {user_id}")
        user_ref = db.collection("users").document(user_id)
        user_ref.set(user_data)
        print("User data stored successfully in Firestore.")

        # Return the generated user ID and data as a response
        return {"id": user_id, "data": user_data}

    except Exception as e:
        # Log the exact error for debugging purposes
        print(f"An error occurred while creating the user: {str(e)}")
        return {"error": f"An error occurred while creating the user: {str(e)}"}