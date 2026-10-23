import random
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Hogwarts: The Interactive Adventure",
    page_icon="⚡",
    layout="centered",
)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "game_stage" not in st.session_state:
  st.session_state.game_stage = "sorting"  # sorting, hub, quest, end
  st.session_state.player_name = ""
  st.session_state.house = ""
  st.session_state.wand = ""
  st.session_state.house_points = 50
  st.session_state.inventory = []
  st.session_state.current_quest = None
  st.session_state.quest_message = ""

# ==========================================
# STAGE 1: THE SORTING CEREMONY & CHARACTER SETUP
# ==========================================
if st.session_state.game_stage == "sorting":
  st.title("🏰 Welcome to Hogwarts!")
  st.image(
      "https://images.unsplash.com/photo-1618944251213-752a5170d0c2?q=80&w=1000&auto=format&fit=crop",
      use_container_width=True,
  )
  st.markdown(
      "The Great Hall is buzzing with excitement. The Sorting Hat sits upon"
      " the stool, waiting for you..."
  )

  with st.form("character_form"):
    name_input = st.text_input(
        "What is your wizarding name?", placeholder="e.g., Harry Potter"
    )

    st.markdown("### Answer the Sorting Hat's Question:")
    question = st.radio(
        "What trait do you value most?",
        [
            "🦁 Bravery & Daring (Gryffindor)",
            "🦅 Wit & Learning (Ravenclaw)",
            "🦡 Loyalty & Patience (Hufflepuff)",
            "🐍 Ambition & Cunning (Slytherin)",
        ],
    )

    wand_choice = st.selectbox(
        "Choose your wand core:",
        [
            "Phoenix Feather (Powerful & Independent)",
            "Dragon Heartstring (Fiery & Strong)",
            "Unicorn Hair (Consistent & Faithful)",
        ],
    )

    submit_button = st.form_submit_button("Put on the Sorting Hat!")

    if submit_button:
      if name_input.strip() == "":
        st.warning("Please enter your name to begin your journey!")
      else:
        st.session_state.player_name = name_input
        st.session_state.wand = wand_choice

        # Assign house based on choice
        if "Gryffindor" in question:
          st.session_state.house = "Gryffindor"
          house_emoji = "🦁"
        elif "Ravenclaw" in question:
          st.session_state.house = "Ravenclaw"
          house_emoji = "🦅"
        elif "Hufflepuff" in question:
          st.session_state.house = "Hufflepuff"
          house_emoji = "🦡"
        else:
          st.session_state.house = "Slytherin"
          house_emoji = "🐍"

        st.success(
            f"The Sorting Hat shouts: **{st.session_state.house.upper()}!**"
            f" {house_emoji}"
        )
        st.balloons()
        st.session_state.game_stage = "hub"
        st.rerun()

# ==========================================
# STAGE 2: HOGWARTS COMMON ROOM & HUB
# ==========================================
elif st.session_state.game_stage == "hub":
  st.title(f"✨ Welcome, {st.session_state.player_name}!")

  # Sidebar Stats Panel
  st.sidebar.header("🧙‍♂️ Wizard Profile")
  st.sidebar.write(f"**Name:** {st.session_state.player_name}")
  st.sidebar.write(f"**House:** {st.session_state.house}")
  st.sidebar.write(f"**Wand:** {st.session_state.wand}")
  st.sidebar.metric(
      label="🏆 House Points", value=st.session_state.house_points
  )
  st.sidebar.write(
      f"**Inventory:** {', '.join(st.session_state.inventory) if st.session_state.inventory else 'Empty'}"
  )

  if st.sidebar.button("Restart Game 🔄"):
    st.session_state.clear()
    st.rerun()

  st.markdown("### Choose Where to Go Today:")

  col1, col2, col3 = st.columns(3)

  with col1:
    if st.button("🧪 Potions Class"):
      st.session_state.game_stage = "potions"
      st.rerun()

  with col2:
    if st.button("🌲 Forbidden Forest"):
      st.session_state.game_stage = "forest"
      st.rerun()

  with col3:
    if st.button("📚 Library Archives"):
      st.session_state.game_stage = "library"
      st.rerun()

  if st.session_state.house_points <= 0:
    st.error(
        "Oh no! Your House Points reached 0. Headmaster Dumbledore is very"
        " disappointed."
    )
    if st.button("Try Again"):
      st.session_state.house_points = 50
      st.rerun()

# ==========================================
# STAGE 3A: POTIONS CLASS MINI-GAME
# ==========================================
elif st.session_state.game_stage == "potions":
  st.header("🧪 Professor Snape's Potions Classroom")
  st.write(
      "Snape glares at you across the dungeon. 'Today, we brew a Cure for"
      " Boils. Select your ingredients carefully...'"
  )

  ingredient = st.selectbox(
      "Choose the main ingredient to add:",
      [
          "Select an ingredient...",
          "Horned Slugs",
          "Powdered Dragon Scale",
          "Bicorn Horn",
      ],
  )

  if st.button("Brew Potion"):
    if ingredient == "Horned Slugs":
      st.success(
          "🎉 Perfect! Snape nods grudgingly. Your potion turns bright pink."
          " +25 House Points!"
      )
      st.session_state.house_points += 25
      st.session_state.inventory.append("Cure for Boils Potion")
    elif ingredient == "Select an ingredient...":
      st.warning("You must pick an ingredient!")
    else:
      st.error(
          "💥 BOOM! The cauldron explodes with green smoke! Snape takes"
          " 20 House Points."
      )
      st.session_state.house_points -= 20

  if st.button("🔙 Back to Common Room"):
    st.session_state.game_stage = "hub"
    st.rerun()

# ==========================================
# STAGE 3B: FORBIDDEN FOREST MINI-GAME
# ==========================================
elif st.session_state.game_stage == "forest":
  st.header("🌲 The Forbidden Forest")
  st.write(
      "You hear a rustling in the dark trees. Suddenly, a giant Acromantula"
      " (spider) drops down blocking your path!"
  )

  spell = st.selectbox(
      "Choose a spell to cast from your wand:",
      ["Select a spell...", "Lumos (Bright Light)", "Arania Exumai (Spider Repelling Spell)", "Wingardium Leviosa (Floating Charm)"],
  )

  if st.button("Cast Spell!"):
    if "Arania Exumai" in spell:
      st.success(
          "✨ A blast of magic hits the spider! It scurries back into the"
          " shadows. You find a rare Phoenix Feather on the ground! +30 House"
          " Points."
      )
      st.session_state.house_points += 30
      st.session_state.inventory.append("Rare Phoenix Feather")
    elif "Select a spell..." in spell:
      st.warning("Quick! Pick a spell!")
    else:
      st.error(
          "❌ That spell didn't work on the giant spider! It chases you back"
          " to the castle gates. -15 House Points."
      )
      st.session_state.house_points -= 15

  if st.button("🔙 Back to Common Room"):
    st.session_state.game_stage = "hub"
    st.rerun()

# ==========================================
# STAGE 3C: LIBRARY ARCHIVES MINI-GAME
# ==========================================
elif st.session_state.game_stage == "library":
  st.header("📚 The Restricted Section")
  st.write(
      "An old, glowing book floats on a pedestal, guarding a wizarding"
      " riddle:"
  )
  st.info(
      "*'I have no voice, but I speak; I have no body, but I come alive with"
      " wind. What am I?'*"
  )

  riddle_answer = st.text_input("Your answer:")

  if st.button("Submit Answer"):
    if riddle_answer.strip().lower() in ["echo", "an echo"]:
      st.success(
          "📖 The book opens wide, revealing ancient spells! +20 House Points."
      )
      st.session_state.house_points += 20
      st.session_state.inventory.append("Ancient Spellbook")
    else:
      st.error("❌ The book snaps shut and floats away. Incorrect!")
      st.session_state.house_points -= 10

  if st.button("🔙 Back to Common Room"):
    st.session_state.game_stage = "hub"
    st.rerun()
