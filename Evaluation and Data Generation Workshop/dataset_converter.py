import json
import sys

def convert_conversations_to_jsonl(json_data):
    # Parse the input JSON string
    data = json.loads(json_data)
    
    # List to store all query-response pairs
    conversation_pairs = []
    
    # Iterate through each conversation object
    for conversation in data:
        # Access the messages array
        messages = conversation['messages']
        
        # Process messages in pairs
        for i in range(0, len(messages) - 1, 2):
            # Get user message (query)
            user_message = messages[i]
            # Get assistant message (response)
            assistant_message = messages[i + 1]
            
            # Verify the roles are correct
            if user_message['role'] == 'user' and assistant_message['role'] == 'assistant':
                # Create a pair in the desired format
                pair = {
                    "query": user_message['content'],
                    "response": assistant_message['content']
                }
                conversation_pairs.append(pair)

    # Convert each pair to JSONL format
    jsonl_output = '\n'.join(json.dumps(pair, ensure_ascii=False) for pair in conversation_pairs)
    return jsonl_output

# Example usage:
if __name__ == "__main__":
    # Assuming the JSON data is stored in a file named 'conversations.json'
    try:
        with open('conversation_starter_output.json', 'r', encoding='utf-8') as f:
            json_data = f.read()
        
        # Convert to JSONL
        jsonl_output = convert_conversations_to_jsonl(json_data)
        
        # Write to output file
        with open('conversation_starter_output.jsonl', 'w', encoding='utf-8') as f:
            f.write(jsonl_output)
            
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")