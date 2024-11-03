import requests
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_write_story():
    # API endpoint URL
    url = "http://localhost:8000/write_story"
    
    # Sample story notes/outline
    story_data = {
        "notes": """
        {"Title":"The Frog Prince of the Swamp","Themes":["Power struggles","Loyalty and betrayal","Love and sacrifice"],"Characters":[{"Name":"King Croak","Description":"The aging king of the frogs, struggling to maintain power in the swamp","Personality":"Wise, proud, and stubborn"},{"Name":"Prince Ribbit","Description":"The prince and heir to the throne, hot-headed and impulsive","Personality":"Adventurous, eager to prove himself, reckless"},{"Name":"Lady Greenleaf","Description":"A mysterious and beautiful frog who becomes Prince Ribbit's love interest","Personality":"Mysterious, seductive, ambitious"},{"Name":"Iago the Toad","Description":"A manipulative and cunning advisor to King Croak, plotting his own rise to power","Personality":"Sly, manipulative, power-hungry"}],"Setting":{"Name":"The Swamp","Description":"A lush, treacherous environment filled with ancient cypress trees, murky waters, and hidden dangers","Features":["The Lily Pad Palace","The Darkwater Marsh","The Witch's Hut"]},"Major Plot Points":[{"Event":"King Croak's Decline","Description":"King Croak's age and health begin to decline, leading to a power vacuum in the swamp","Consequences":"Prince Ribbit sees an opportunity to prove himself and takes actions without the king's guidance"},{"Event":"The Appearance of Lady Greenleaf","Description":"Lady Greenleaf arrives in the swamp, captivating Prince Ribbit with her charm and beauty","Consequences":"Prince Ribbit becomes distracted and distant from his royal duties, leading Iago to whisper fuel-driven ambitions into his ears"},{"Event":"The Betrayal of Iago","Description":"Iago is revealed to be working against the royal family, seeking to use the chaos to take the throne for himself","Consequences":"King Croak is forced to make a difficult decision, leading to a tragic confrontation that will decide the future of the swamp"},{"Event":"The Confrontation at the Witch's Hut","Description":"Prince Ribbit and Iago face off in a final showdown at the Witch's Hut, with the fate of the swamp hanging in the balance","Consequences":"The true nature of Lady Greenleaf is revealed, and the prince must make a choice that will define his future as the leader of the swamp"}]}
        """
    }
    
    # Make POST request
    response = requests.post(url, json=story_data)
    
    # Print response
    if response.status_code == 200:
        print("Story generated successfully!")
        print("\nGenerated Story:")
        print(response.json()["story"])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_lookup_news():
    url = "http://localhost:8000/copilotkit"
    response = requests.post(url, json={"query": "Apple"})
    print(response.json())

def test_create_story_outline():
    url = "http://localhost:8000/create_story_outline"
    conversation = '''
    {
        "assistant": "What is the story about?",
        "user": "It's about a frog king is getting old and needs a successor as ruler of the swamp.",
        "assistant": "Interesting, what are the main characters?",
        "user": "There's the frog king, his son the prince, a beautiful frog lady who is the prince's love interest, and a toad advisor who is trying to take over the swamp.",
        "assistant": "What is the setting of the story?",
        "user": "The story is set in a swamp with ancient cypress trees, murky waters, and hidden dangers.",
        "assistant": "What are the major plot points of the story?",
        "user": "There's the frog king's decline, the appearance of the beautiful frog lady, the betrayal of the toad advisor, and a final confrontation at the witch's hut."
    }
    '''
    previous_outline = '''
        {"Title":"The Doggy Prince of the Beach","Themes":["Power struggles","Loyalty and betrayal","Puppy love"],"Characters":[{"Name":"Air Bud","Description":"A golden retriever who plays basketball"},{"Name":"Prince Rabbit","Description":"The prince and a hare"},{"Name":"Lady Greenleaf","Description":"A mysterious and beautiful frog who becomes Prince Ribbit's love interest"},{"Name":"Iago the Toad","Description":"A manipulative and cunning advisor to King Croak and Air Bud's best friend."}],"Setting":"Connecticut","Major Plot Points":["Beach party","Air Bud's basketball game","Iago's betrayal","Final confrontation"]}
    '''
    data = {
        "conversation": conversation,
        "previous_outline": previous_outline
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Story outline created successfully!")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")

if __name__ == "__main__":
    test_create_story_outline()