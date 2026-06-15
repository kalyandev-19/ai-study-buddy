import sys
import utils

API_KEY = "***REMOVED***"

def run_tests():
    print("Starting AI Feature Verification Tests...")
    print("------------------------------------------")
    
    # Test 1: Explain Concept
    print("Testing 'Explain Concept'...")
    try:
        explanation = utils.explain_concept(API_KEY, "Photosynthesis", "Grade School (Explain Like I'm 5)", "Simple & Direct")
        if "API Error" in explanation:
            print(f"❌ Explain Concept Failed: {explanation}")
            return False
        print("✅ Explain Concept Succeeded!")
        print(explanation[:200] + "...\n")
    except Exception as e:
        print(f"❌ Explain Concept Raised Exception: {str(e)}")
        return False
        
    # Test 2: Summarize Notes
    print("Testing 'Summarize Notes'...")
    try:
        notes = "Mitosis is a part of the cell cycle in which replicated chromosomes are separated into two new nuclei. Cell division gives rise to genetically identical cells in which the total number of chromosomes is maintained."
        summary = utils.summarize_notes(API_KEY, notes)
        if "API Error" in summary:
            print(f"❌ Summarize Notes Failed: {summary}")
            return False
        print("✅ Summarize Notes Succeeded!")
        print(summary[:200] + "...\n")
    except Exception as e:
        print(f"❌ Summarize Notes Raised Exception: {str(e)}")
        return False
        
    # Test 3: Generate Flashcards
    print("Testing 'Generate Flashcards'...")
    try:
        cards = utils.generate_flashcards(API_KEY, "Python Functions", 3)
        if not isinstance(cards, list) or (cards and "error" in str(cards[0]).lower()):
            print(f"❌ Generate Flashcards Failed: {cards}")
            return False
        print("✅ Generate Flashcards Succeeded!")
        print(f"Sample Card Front: {cards[0].get('front')}")
        print(f"Sample Card Back: {cards[0].get('back')}\n")
    except Exception as e:
        print(f"❌ Generate Flashcards Raised Exception: {str(e)}")
        return False

    # Test 4: Generate Quiz
    print("Testing 'Generate Quiz'...")
    try:
        quiz = utils.generate_quiz(API_KEY, "Gravity", 3)
        if not isinstance(quiz, list) or (quiz and "error" in str(quiz[0]).lower()):
            print(f"❌ Generate Quiz Failed: {quiz}")
            return False
        print("✅ Generate Quiz Succeeded!")
        print(f"Sample Question: {quiz[0].get('question')}")
        print(f"Options: {quiz[0].get('options')}")
        print(f"Answer Index: {quiz[0].get('answer')}")
        print(f"Explanation: {quiz[0].get('explanation')}\n")
    except Exception as e:
        print(f"❌ Generate Quiz Raised Exception: {str(e)}")
        return False
        
    # Test 5: Study Chat
    print("Testing 'Study Chat'...")
    try:
        history = [{"role": "user", "content": "Hello! I want to study cell biology."}]
        reply = utils.ask_study_chat(API_KEY, history, "What is the mitochondria?")
        if "API Error" in reply:
            print(f"❌ Study Chat Failed: {reply}")
            return False
        print("✅ Study Chat Succeeded!")
        print(reply[:200] + "...\n")
    except Exception as e:
        print(f"❌ Study Chat Raised Exception: {str(e)}")
        return False
        
    print("------------------------------------------")
    print("🎉 All AI features verified successfully!")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
