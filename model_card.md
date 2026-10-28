# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Stress test output

Terminal output from `python -m src.main` for each profile I tested (top 5 songs each):

**Pop / Happy**

```
============================================================
  Profile: Pop / Happy
  genre=pop | mood=happy | energy=0.80 | acoustic=no | instrumental=no
============================================================

  #1  Sunrise City  (Neon Echo)
      Score: 4.98 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.98)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #2  Gym Hero  (Max Pulse)
      Score: 3.87 / 5.00
      Why:
        - genre match (+2.0)
        - energy close to target (+0.87)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Rooftop Lights  (Indigo Parade)
      Score: 2.96 / 5.00
      Why:
        - mood match (+1.0)
        - energy close to target (+0.96)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Concrete Crown  (Verse Theory)
      Score: 1.98 / 5.00
      Why:
        - energy close to target (+0.98)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Fiesta de Fuego  (Los Brillantes)
      Score: 1.95 / 5.00
      Why:
        - energy close to target (+0.95)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Study Session**

```
============================================================
  Profile: Study Session
  genre=lofi | mood=chill | energy=0.40 | acoustic=yes | instrumental=yes
============================================================

  #1  Midnight Coding  (LoRoom)
      Score: 4.98 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.98)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #2  Library Rain  (Paper Lanterns)
      Score: 4.95 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.95)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Focus Flow  (LoRoom)
      Score: 4.00 / 5.00
      Why:
        - genre match (+2.0)
        - energy close to target (+1.00)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Spacewalk Thoughts  (Orbit Bloom)
      Score: 2.88 / 5.00
      Why:
        - mood match (+1.0)
        - energy close to target (+0.88)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Coffee Shop Stories  (Slow Stereo)
      Score: 1.97 / 5.00
      Why:
        - energy close to target (+0.97)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Deep Intense Rock**

```
============================================================
  Profile: Deep Intense Rock
  genre=rock | mood=intense | energy=0.90 | acoustic=no | instrumental=no
============================================================

  #1  Storm Runner  (Voltline)
      Score: 4.99 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.99)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #2  Gym Hero  (Max Pulse)
      Score: 2.97 / 5.00
      Why:
        - mood match (+1.0)
        - energy close to target (+0.97)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Fiesta de Fuego  (Los Brillantes)
      Score: 1.95 / 5.00
      Why:
        - energy close to target (+0.95)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Iron Tempest  (Grave Signal)
      Score: 1.93 / 5.00
      Why:
        - energy close to target (+0.93)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Sunrise City  (Neon Echo)
      Score: 1.92 / 5.00
      Why:
        - energy close to target (+0.92)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Edge Case: Sad but Hyped**

```
============================================================
  Profile: Edge Case: Sad but Hyped
  genre=folk | mood=sad | energy=0.90 | acoustic=no | instrumental=no
============================================================

  #1  Letters I Never Sent  (Hollow Pines)
      Score: 3.84 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.34)
        - instrumental preference match (+0.5)

  #2  Storm Runner  (Voltline)
      Score: 1.99 / 5.00
      Why:
        - energy close to target (+0.99)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Gym Hero  (Max Pulse)
      Score: 1.97 / 5.00
      Why:
        - energy close to target (+0.97)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Fiesta de Fuego  (Los Brillantes)
      Score: 1.95 / 5.00
      Why:
        - energy close to target (+0.95)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Iron Tempest  (Grave Signal)
      Score: 1.93 / 5.00
      Why:
        - energy close to target (+0.93)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Edge Case: Acoustic Headbanger**

```
============================================================
  Profile: Edge Case: Acoustic Headbanger
  genre=metal | mood=angry | energy=0.95 | acoustic=yes | instrumental=yes
============================================================

  #1  Iron Tempest  (Grave Signal)
      Score: 3.98 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.98)

  #2  Laser Bloom  (Kilowatt Kids)
      Score: 1.50 / 5.00
      Why:
        - energy close to target (+1.00)
        - instrumental preference match (+0.5)

  #3  Midnight Coding  (LoRoom)
      Score: 1.47 / 5.00
      Why:
        - energy close to target (+0.47)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Focus Flow  (LoRoom)
      Score: 1.45 / 5.00
      Why:
        - energy close to target (+0.45)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Coffee Shop Stories  (Slow Stereo)
      Score: 1.42 / 5.00
      Why:
        - energy close to target (+0.42)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Edge Case: Capital Letters**

```
============================================================
  Profile: Edge Case: Capital Letters
  genre=Pop | mood=Happy | energy=0.80 | acoustic=no | instrumental=no
============================================================

  #1  Sunrise City  (Neon Echo)
      Score: 1.98 / 5.00
      Why:
        - energy close to target (+0.98)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #2  Concrete Crown  (Verse Theory)
      Score: 1.98 / 5.00
      Why:
        - energy close to target (+0.98)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Rooftop Lights  (Indigo Parade)
      Score: 1.96 / 5.00
      Why:
        - energy close to target (+0.96)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Fiesta de Fuego  (Los Brillantes)
      Score: 1.95 / 5.00
      Why:
        - energy close to target (+0.95)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Storm Runner  (Voltline)
      Score: 1.89 / 5.00
      Why:
        - energy close to target (+0.89)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Edge Case: Not in Catalog**

```
============================================================
  Profile: Edge Case: Not in Catalog
  genre=k-pop | mood=dreamy | energy=0.70 | acoustic=no | instrumental=no
============================================================

  #1  Rooftop Lights  (Indigo Parade)
      Score: 1.94 / 5.00
      Why:
        - energy close to target (+0.94)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #2  Concrete Crown  (Verse Theory)
      Score: 1.92 / 5.00
      Why:
        - energy close to target (+0.92)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Island Sunday  (Coral Roots)
      Score: 1.90 / 5.00
      Why:
        - energy close to target (+0.90)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Sunrise City  (Neon Echo)
      Score: 1.88 / 5.00
      Why:
        - energy close to target (+0.88)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Velvet Promises  (Amara Soul)
      Score: 1.85 / 5.00
      Why:
        - energy close to target (+0.85)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

**Edge Case: Energy Too High**

```
============================================================
  Profile: Edge Case: Energy Too High
  genre=edm | mood=euphoric | energy=1.50 | acoustic=no | instrumental=no
============================================================

  #1  Laser Bloom  (Kilowatt Kids)
      Score: 3.95 / 5.00
      Why:
        - genre match (+2.0)
        - mood match (+1.0)
        - energy close to target (+0.45)
        - acoustic preference match (+0.5)

  #2  Iron Tempest  (Grave Signal)
      Score: 1.47 / 5.00
      Why:
        - energy close to target (+0.47)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #3  Gym Hero  (Max Pulse)
      Score: 1.43 / 5.00
      Why:
        - energy close to target (+0.43)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #4  Storm Runner  (Voltline)
      Score: 1.41 / 5.00
      Why:
        - energy close to target (+0.41)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)

  #5  Fiesta de Fuego  (Los Brillantes)
      Score: 1.35 / 5.00
      Why:
        - energy close to target (+0.35)
        - acoustic preference match (+0.5)
        - instrumental preference match (+0.5)
```

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
