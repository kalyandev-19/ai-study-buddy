import os
import streamlit as st
import utils

# Page Configuration
st.set_page_config(
    page_title="AI-Powered Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session States
session_states = {
    "api_key": "***REMOVED***",
    "notes_text": "",
    "notes_summary": "",
    
    # Flashcard States
    "flashcards": [],
    "current_card_idx": 0,
    "card_flipped": False,
    "flashcard_learned_status": {},  # card_index -> True/False
    
    # Quiz States
    "quiz": [],
    "quiz_user_answers": {},  # question_idx -> option_idx
    "quiz_submitted": False,
    "quiz_score": 0,
    
    # Chat States
    "chat_history": []  # list of {"role": "user"/"model", "content": "..."}
}

for key, val in session_states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar Layout
with st.sidebar:
    st.markdown("### 📚 Study Materials Source")
    st.markdown(
        "When notes are uploaded or pasted in the **Summarize Notes** tab, they will become "
        "available as source material for generating flashcards and quizzes."
    )
    st.markdown(
        """
        📚 AI Study Buddy Features Description

        1. PDF Notes Upload & Processing
        Users can upload study materials in PDF format. The system automatically extracts text content,
        cleans the data, and prepares it for intelligent search and analysis.

        Benefits:
        - Supports digital learning materials
        - Eliminates manual note organization
        - Enables AI-powered learning assistance

        2. Intelligent Question Answering (RAG)
        The application uses Retrieval-Augmented Generation (RAG) to answer questions based on uploaded notes.
        Instead of providing generic AI responses, it retrieves relevant content from the study material and
        generates accurate, context-aware answers.

        Benefits:
        - Answers are based on user-provided notes
        - Improves accuracy and relevance
        - Reduces hallucinations from AI models

        3. AI-Powered Quiz Generation
        The system automatically generates quizzes from uploaded study materials, including multiple-choice
        questions, short-answer questions, and concept-based assessments.

        Benefits:
        - Reinforces learning through self-assessment
        - Helps identify knowledge gaps
        - Supports exam preparation

        4. Flashcard Creation
        The application converts important concepts into question-and-answer flashcards for active recall learning.

        Benefits:
        - Improves memory retention
        - Simplifies revision sessions
        - Encourages active learning techniques
        """
    )
    
    if st.session_state.notes_text:
        st.success("✅ Notes loaded in session")
        char_count = len(st.session_state.notes_text)
        st.info(f"Source size: {char_count} characters")
        if st.button("Reset Session Notes"):
            st.session_state.notes_text = ""
            st.session_state.notes_summary = ""
            st.session_state.flashcards = []
            st.session_state.quiz = []
            st.rerun()

# Main Application Title
st.markdown("<h1 class='gradient-header'>🎓 AI-Powered Study Buddy</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #94a3b8; font-size: 1.15rem; margin-bottom: 2rem;'>"
    "Explain complex concepts, summarize files, and generate interactive quizzes or flashcards instantly using AI."
    "</p>",
    unsafe_allow_html=True
)

# Check API Key
has_api_key = len(st.session_state.api_key.strip()) > 0

# App Tabs
tab_dashboard, tab_explain, tab_summarize, tab_flashcards, tab_quiz, tab_chat = st.tabs([
    "📂 Dashboard", 
    "💡 Explain Concept", 
    "📝 Summarize Notes", 
    "🎴 Flashcards", 
    "⚔️ Quiz Arena", 
    "💬 Study Chat"
])

# ----------------- TABS IMPLEMENTATION -----------------

# 1. DASHBOARD
with tab_dashboard:
    st.markdown("### Welcome to your AI Study Hub!")
    st.markdown(
        "Select a module below or use the navigation tabs above to start studying efficiently."
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="dashboard-card-title">💡 Explain Concept</div>
                <div class="dashboard-card-desc">
                    Enter any complex topic (e.g. "Quantum Computing", "Mitosis") and choose a tailored depth level. 
                    Get simplified explanations, custom analogies, and step-by-step breakdowns.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Go to Explanations", key="dash_btn_explain", use_container_width=True):
            # Streamlit doesn't support easy tab changes programmatic-wise without experimental query params,
            # so we guide the user to the tab or tell them to select it.
            st.info("Please select the '💡 Explain Concept' tab at the top!")

    with col2:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="dashboard-card-title">📝 Summarize Notes</div>
                <div class="dashboard-card-desc">
                    Upload long PDF files or paste your text notes. Get a condensed overview, 
                    bulleted key takeaways, and an automated glossary of important terms.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Go to Summaries", key="dash_btn_summarize", use_container_width=True):
            st.info("Please select the '📝 Summarize Notes' tab at the top!")

    with col3:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="dashboard-card-title">🎴 Interactive Flashcards</div>
                <div class="dashboard-card-desc">
                    Create flashcards dynamically from any topic or from your uploaded notes. 
                    Practice with interactive 3D card flips and mark cards as learned to track progress.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Go to Flashcards", key="dash_btn_flashcards", use_container_width=True):
            st.info("Please select the '🎴 Flashcards' tab at the top!")

    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="dashboard-card-title">⚔️ Quiz Arena</div>
                <div class="dashboard-card-desc">
                    Test your understanding with AI-generated multiple-choice questions. 
                    Receive immediate grading, correct answers, and thorough explanations.
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Go to Quiz Arena", key="dash_btn_quiz", use_container_width=True):
            st.info("Please select the '⚔️ Quiz Arena' tab at the top!")

    with col5:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="dashboard-card-title">💬 Study Chat</div>
                <div class="dashboard-card-desc">
                    Have follow-up questions or need instant clarification on a topic? 
                    Chat directly with your virtual study buddy. It remembers your chat history!
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Go to Study Chat", key="dash_btn_chat", use_container_width=True):
            st.info("Please select the '💬 Study Chat' tab at the top!")
            
    with col6:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="dashboard-card-title">🚀 Ready to Learn</div>
                <div class="dashboard-card-desc">
                    Your Study Buddy is active! All AI features are powered by your pre-configured Gemini API Key. 
                    Switch between tabs to start studying.
                </div>
            </div>
            """, unsafe_allow_html=True
        )

# 2. EXPLAIN CONCEPT
with tab_explain:
    st.markdown("### 💡 Understand Complex Concepts")
    st.write("Enter a concept or topic you are currently learning, and let the Study Buddy explain it.")
    
    if not has_api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar to use this feature.")
    else:
        topic_input = st.text_input("Enter Topic/Concept:", placeholder="e.g. Photosynthesis, Blockchain, Theory of Relativity")
        
        col_lvl, col_sty = st.columns(2)
        with col_lvl:
            audience_level = st.selectbox(
                "Audience Level (Explain Like I'm...):",
                ["Grade School (Explain Like I'm 5)", "High School Student", "College Student", "Expert Practitioner"]
            )
        with col_sty:
            explanation_style = st.selectbox(
                "Explanation Style:",
                ["Simple & Direct", "Analogy-rich (uses real-world comparisons)", "Step-by-step Breakdown", "Storytelling / Narrative format"]
            )
            
        if st.button("Explain to Me!", type="primary"):
            if not topic_input.strip():
                st.error("Please enter a valid topic.")
            else:
                with st.spinner("Analyzing and simplifying..."):
                    explanation = utils.explain_concept(
                        st.session_state.api_key,
                        topic_input,
                        audience_level,
                        explanation_style
                    )
                    st.markdown("---")
                    st.markdown(explanation)


# 3. SUMMARIZE NOTES
with tab_summarize:
    st.markdown("### 📝 Study Notes Summarizer")
    st.write("Convert long-form text or documents into structured summaries, key takeaways, and glossary lists.")
    
    if not has_api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar to use this feature.")
    else:
        input_type = st.radio("Choose Input Method:", ["Upload File", "Paste Text"], horizontal=True)
        notes_input = ""
        
        if input_type == "Upload File":
            uploaded_file = st.file_uploader("Upload a study document (.txt or .pdf):", type=["txt", "pdf"])
            if uploaded_file is not None:
                with st.spinner("Extracting text from file..."):
                    file_bytes = uploaded_file.read()
                    if uploaded_file.name.endswith(".pdf"):
                        notes_input = utils.extract_text_from_pdf(file_bytes)
                    else:
                        notes_input = file_bytes.decode("utf-8", errors="ignore")
                    
                    if notes_input.startswith("Error"):
                        st.error(notes_input)
                        notes_input = ""
                    else:
                        st.success(f"Successfully extracted notes from '{uploaded_file.name}'!")
        else:
            notes_input = st.text_area("Paste your study notes or article text here:", height=250, placeholder="Paste details here...")
            
        if st.button("Summarize & Analyze Notes", type="primary"):
            if not notes_input.strip():
                st.error("Please enter or upload study notes.")
            else:
                st.session_state.notes_text = notes_input
                with st.spinner("Generating structured summary..."):
                    summary_output = utils.summarize_notes(
                        st.session_state.api_key,
                        notes_input
                    )
                    st.session_state.notes_summary = summary_output
                    st.rerun()
                    
        if st.session_state.notes_summary:
            st.markdown("---")
            st.markdown(st.session_state.notes_summary)


# 4. FLASHCARDS
with tab_flashcards:
    st.markdown("### 🎴 Interactive Study Flashcards")
    st.write("Practice your knowledge with active recall! Flip cards to check answers, and mark them as learned.")
    
    if not has_api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar to use this feature.")
    else:
        # Source Selection
        has_session_notes = len(st.session_state.notes_text.strip()) > 0
        source_mode = "Manual Input"
        
        if has_session_notes:
            source_mode = st.radio(
                "Select Material Source for Flashcards:",
                ["Use my Uploaded Notes", "Enter a Specific Topic"],
                horizontal=True,
                key="fc_source"
            )
            
        # Generating Flashcards
        if not st.session_state.flashcards:
            st.info("No active flashcard deck. Let's generate one!")
            
            if source_mode == "Use my Uploaded Notes":
                num_cards = st.slider("Number of cards:", min_value=3, max_value=10, value=5, key="fc_num_notes")
                if st.button("Generate Flashcards from Notes", type="primary"):
                    with st.spinner("Creating flashcard deck..."):
                        cards = utils.generate_flashcards(
                            st.session_state.api_key,
                            st.session_state.notes_text,
                            num_cards
                        )
                        st.session_state.flashcards = cards
                        st.session_state.current_card_idx = 0
                        st.session_state.card_flipped = False
                        st.session_state.flashcard_learned_status = {}
                        st.rerun()
            else:
                fc_topic = st.text_input("Enter Topic for Flashcards:", placeholder="e.g. JavaScript Closures, French Revolution, Organic Chemistry")
                num_cards = st.slider("Number of cards:", min_value=3, max_value=10, value=5, key="fc_num_topic")
                if st.button("Generate Topic Flashcards", type="primary"):
                    if not fc_topic.strip():
                        st.error("Please enter a topic name.")
                    else:
                        with st.spinner(f"Creating flashcards for '{fc_topic}'..."):
                            cards = utils.generate_flashcards(
                                st.session_state.api_key,
                                fc_topic,
                                num_cards
                            )
                            st.session_state.flashcards = cards
                            st.session_state.current_card_idx = 0
                            st.session_state.card_flipped = False
                            st.session_state.flashcard_learned_status = {}
                            st.rerun()
        else:
            # Active Flashcard Deck Player
            cards = st.session_state.flashcards
            idx = st.session_state.current_card_idx
            card = cards[idx]
            
            # Progress bar
            progress = (idx + 1) / len(cards)
            st.progress(progress, text=f"Card {idx + 1} of {len(cards)}")
            
            # HTML Card render with flipping logic
            flip_class = "flipped" if st.session_state.card_flipped else ""
            
            st.markdown(
                f"""
                <div class="flashcard-wrapper">
                    <div class="flashcard-inner {flip_class}">
                        <!-- FRONT FACE -->
                        <div class="flashcard-face flashcard-front">
                            <div class="flashcard-side-indicator">Question</div>
                            <div class="flashcard-text">{card['front']}</div>
                        </div>
                        <!-- BACK FACE -->
                        <div class="flashcard-face flashcard-back">
                            <div class="flashcard-side-indicator">Answer</div>
                            <div class="flashcard-text">{card['back']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True
            )
            
            # Action controls below card
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            
            with btn_col2:
                # Flip action
                if st.button("🔄 Flip Card", use_container_width=True, type="secondary"):
                    st.session_state.card_flipped = not st.session_state.card_flipped
                    st.rerun()
            
            # Sub-controls for status
            st.markdown("<br>", unsafe_allow_html=True)
            status_col1, status_col2 = st.columns(2)
            
            # Track status
            is_learned = st.session_state.flashcard_learned_status.get(idx, False)
            
            with status_col1:
                if st.button("✅ I Know This!", use_container_width=True, type="primary" if is_learned else "secondary"):
                    st.session_state.flashcard_learned_status[idx] = True
                    # Auto advance on marking learned if not last
                    if idx < len(cards) - 1:
                        st.session_state.current_card_idx += 1
                        st.session_state.card_flipped = False
                    st.rerun()
                    
            with status_col2:
                if st.button("❌ Need to Review", use_container_width=True, type="primary" if not is_learned and idx in st.session_state.flashcard_learned_status else "secondary"):
                    st.session_state.flashcard_learned_status[idx] = False
                    if idx < len(cards) - 1:
                        st.session_state.current_card_idx += 1
                        st.session_state.card_flipped = False
                    st.rerun()
            
            # Navigation Controls
            st.markdown("---")
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            with nav_col1:
                if st.button("⬅️ Previous", disabled=(idx == 0), use_container_width=True):
                    st.session_state.current_card_idx -= 1
                    st.session_state.card_flipped = False
                    st.rerun()
            with nav_col3:
                if st.button("Next ➡️", disabled=(idx == len(cards) - 1), use_container_width=True):
                    st.session_state.current_card_idx += 1
                    st.session_state.card_flipped = False
                    st.rerun()
            with nav_col2:
                if st.button("🧹 Clear Deck & Start Over", use_container_width=True):
                    st.session_state.flashcards = []
                    st.session_state.current_card_idx = 0
                    st.session_state.card_flipped = False
                    st.session_state.flashcard_learned_status = {}
                    st.rerun()
            
            # Score Tracker
            learned_count = sum(1 for status in st.session_state.flashcard_learned_status.values() if status)
            st.write(f"🎯 **Deck Mastery:** {learned_count} / {len(cards)} cards mastered.")


# 5. QUIZ ARENA
with tab_quiz:
    st.markdown("### ⚔️ Quiz Arena")
    st.write("Challenge yourself with multiple-choice tests generated based on your topic or study notes.")
    
    if not has_api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar to use this feature.")
    else:
        # Source Selection
        has_session_notes = len(st.session_state.notes_text.strip()) > 0
        quiz_source_mode = "Manual Input"
        
        if has_session_notes:
            quiz_source_mode = st.radio(
                "Select Material Source for Quiz:",
                ["Use my Uploaded Notes", "Enter a Specific Topic"],
                horizontal=True,
                key="quiz_source"
            )
            
        # Generating Quiz
        if not st.session_state.quiz:
            st.info("No active quiz. Let's create one!")
            
            if quiz_source_mode == "Use my Uploaded Notes":
                num_q = st.slider("Number of questions:", min_value=3, max_value=10, value=5, key="quiz_num_notes")
                if st.button("Generate Quiz from Notes", type="primary"):
                    with st.spinner("Crafting quiz questions..."):
                        quiz_data = utils.generate_quiz(
                            st.session_state.api_key,
                            st.session_state.notes_text,
                            num_q
                        )
                        st.session_state.quiz = quiz_data
                        st.session_state.quiz_user_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = 0
                        st.rerun()
            else:
                quiz_topic = st.text_input("Enter Topic for Quiz:", placeholder="e.g. Mitochondria structure, Python Data Structures, WW2 details")
                num_q = st.slider("Number of questions:", min_value=3, max_value=10, value=5, key="quiz_num_topic")
                if st.button("Generate Topic Quiz", type="primary"):
                    if not quiz_topic.strip():
                        st.error("Please enter a topic.")
                    else:
                        with st.spinner(f"Crafting quiz for '{quiz_topic}'..."):
                            quiz_data = utils.generate_quiz(
                                st.session_state.api_key,
                                quiz_topic,
                                num_q
                            )
                            st.session_state.quiz = quiz_data
                            st.session_state.quiz_user_answers = {}
                            st.session_state.quiz_submitted = False
                            st.session_state.quiz_score = 0
                            st.rerun()
        else:
            # Active Quiz Taking
            quiz = st.session_state.quiz
            submitted = st.session_state.quiz_submitted
            
            st.write("📝 Select the best answer for each question:")
            
            for i, item in enumerate(quiz):
                st.markdown(f"#### Question {i+1}: {item['question']}")
                
                # Check if we should disable choices (if submitted)
                options = item['options']
                
                # Default selection (none selected initially)
                current_selection = st.session_state.quiz_user_answers.get(i, None)
                
                if submitted:
                    correct_idx = item['answer']
                    selected_idx = current_selection
                    
                    # Highlight selected options and correctness
                    for opt_idx, opt in enumerate(options):
                        is_selected = selected_idx == opt_idx
                        is_correct = correct_idx == opt_idx
                        
                        if is_selected and is_correct:
                            st.success(f"👉 **{opt}** (Your correct choice!)")
                        elif is_selected and not is_correct:
                            st.error(f"👉 **{opt}** (Your incorrect choice)")
                        elif is_correct:
                            st.info(f"💡 **{opt}** (Correct answer)")
                        else:
                            st.text(f"⚪ {opt}")
                            
                    # Detailed feedback box
                    if selected_idx == correct_idx:
                        st.markdown(
                            f"""
                            <div class="quiz-feedback-correct">
                                <strong>🎉 Correct!</strong><br>
                                {item['explanation']}
                            </div>
                            """, unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="quiz-feedback-incorrect">
                                <strong>❌ Incorrect</strong> (Selected Option {chr(65 + (selected_idx if selected_idx is not None else 0)) if selected_idx is not None else "None"})<br>
                                {item['explanation']}
                            </div>
                            """, unsafe_allow_html=True
                        )
                else:
                    # Renders active interactive inputs
                    options_dict = {f"{chr(65+idx)}. {val}": idx for idx, val in enumerate(options)}
                    
                    # Compute preselection index
                    index_prefill = None
                    if current_selection is not None:
                        index_prefill = current_selection
                        
                    selected_label = st.radio(
                        f"Select option for Question {i+1}:",
                        options=list(options_dict.keys()),
                        index=index_prefill,
                        key=f"q_radio_{i}",
                        label_visibility="collapsed"
                    )
                    
                    if selected_label:
                        st.session_state.quiz_user_answers[i] = options_dict[selected_label]
                        
                st.markdown("---")
                
            # Submit or Reset actions
            if not submitted:
                if st.button("Submit My Answers", type="primary", use_container_width=True):
                    # Calculate Score
                    score = 0
                    for idx, item in enumerate(quiz):
                        user_ans = st.session_state.quiz_user_answers.get(idx, None)
                        if user_ans == item['answer']:
                            score += 1
                    
                    st.session_state.quiz_score = score
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                score = st.session_state.quiz_score
                total = len(quiz)
                pct = (score / total) * 100
                
                # Glowing Score Result card
                st.markdown(
                    f"""
                    <div class="dashboard-card" style="text-align: center; border-color: rgba(99, 102, 241, 0.4);">
                        <h2 style="color: #a5b4fc;">Quiz Completed!</h2>
                        <h1 class="gradient-header" style="font-size: 3.5rem; margin: 15px 0;">{score} / {total}</h1>
                        <p style="font-size: 1.25rem; color: #cbd5e1;">Score: <strong>{pct:.1f}%</strong></p>
                    </div>
                    """, unsafe_allow_html=True
                )
                
                col_actions1, col_actions2 = st.columns(2)
                with col_actions1:
                    if st.button("🔁 Retake This Quiz", use_container_width=True):
                        st.session_state.quiz_user_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = 0
                        st.rerun()
                with col_actions2:
                    if st.button("🧹 Clear & Generate New Quiz", use_container_width=True):
                        st.session_state.quiz = []
                        st.session_state.quiz_user_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = 0
                        st.rerun()


# 6. STUDY CHAT
with tab_chat:
    st.markdown("### 💬 Study Chatbot")
    st.write("Ask follow-up questions, request coding examples, or clear up doubts about your studies.")
    
    if not has_api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar to use this feature.")
    else:
        # Display Message History
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Send new message input
        user_query = st.chat_input("Ask a follow-up question here...")
        if user_query:
            # Render user message instantly
            with st.chat_message("user"):
                st.markdown(user_query)
                
            # Add to state history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    reply = utils.ask_study_chat(
                        st.session_state.api_key,
                        st.session_state.chat_history[:-1], # pass historical messages excluding the last one which was just added
                        user_query
                    )
                    st.markdown(reply)
                    
            st.session_state.chat_history.append({"role": "model", "content": reply})
            st.rerun()
            
        # Clear chat history button
        if st.session_state.chat_history:
            if st.button("Clear Chat Conversation", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()