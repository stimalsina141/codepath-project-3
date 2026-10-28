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

The biggest weakness I found is that the "likes acoustic" setting secretly works like a "likes calm music" switch. In my catalog, every acoustic song has an energy of 0.52 or lower, and every non-acoustic song has an energy of 0.55 or higher, so there's no such thing as a loud acoustic song or a quiet electronic one. When I tested an "Acoustic Headbanger" profile (angry metal, energy 0.95, likes acoustic), three of the top five were calm lofi and jazz study songs, because the +0.5 acoustic bonus pulled them up. So people whose taste crosses that line, like someone who loves energetic acoustic folk-rock or calm electronic music, can't really be served, and they get pushed toward whatever is "normal" for their side. It's a small filter bubble that comes from the data, not from the code itself.

Other weaknesses I noticed:

- Genre and mood only count if the words match exactly, so "metal" gets nothing for a rock fan, "indie pop" gets nothing for a pop fan, and even "Pop" with a capital P gets nothing.
- Most genres only have one song. A lofi fan gets three real matches, but a rock fan gets one, and the rest of the list is filler.
- It never looks at whether a song sounds happy or sad (valence), so it can't tell a calm sad song from a calm happy one.

---

## 7. Evaluation  

**Profiles I tested**

I tested 3 normal profiles and 5 "edge case" profiles that were meant to trick the system:

- **Pop / Happy:** upbeat pop with singing, energy 0.80
- **Study Session:** calm lofi with no singing, energy 0.40
- **Deep Intense Rock:** loud rock with singing, energy 0.90
- **Sad but Hyped:** wants sad folk songs but at energy 0.90
- **Acoustic Headbanger:** wants angry metal at energy 0.95, but also acoustic and no singing
- **Capital Letters:** the same as Pop / Happy, just typed as "Pop" and "Happy"
- **Not in Catalog:** wants "k-pop" and "dreamy", which no song has
- **Energy Too High:** wants energy 1.5, which is outside the 0 to 1 range

For each one I checked if the #1 song made sense, if the rest of the top 5 felt like something that person would actually want, and if the reasons explained the score.

**What surprised me**

- One capital letter broke everything. "Pop" isn't the same as "pop" to the program, so Sunrise City dropped from 4.98 to 1.98 and Gym Hero disappeared from the list.
- Fiesta de Fuego showed up in 5 of the 8 top-5 lists. It's a loud song with singing, so once the real matches run out it fills the empty spots for almost anyone who wants high energy.
- An energy target of 1.5 gave some songs negative points. Moonlit Sonata got -0.32 for energy, and the reason printed as "+-0.32".
- Changing the weights barely changed anything (see the experiment below).

**Why "Gym Hero" shows up for someone who wants Happy Pop**

Gym Hero is a pop song, so it gets the biggest reward right away: 2 points for matching the genre. It's also loud, has singing, and isn't acoustic, which is exactly what this person asked for, so it picks up almost every other point too. The only thing it misses is the mood, because it's "intense" instead of "happy," and that only costs 1 point. A happy song that isn't labeled "pop" loses 2 points instead, so Gym Hero ends up at #2 (3.87) ahead of Rooftop Lights, a happy indie pop song (2.96). The system basically trusts the genre label more than the feeling of the song.

**Comparing profiles to each other**

- **Pop / Happy vs. Study Session:** Their lists have zero songs in common. Pop / Happy gets loud songs with singing (energy 0.76 to 0.93), and Study Session gets calm acoustic songs with no singing (energy 0.28 to 0.42). This makes sense because the two profiles are opposite on every setting.
- **Study Session vs. Deep Intense Rock:** Each one's favorite songs are at the bottom of the other's list. Storm Runner is #1 for rock but #18 for the study listener, and the lofi songs land between #15 and #18 for the rock fan. That's what should happen for two opposite tastes.
- **Pop / Happy vs. Deep Intense Rock:** They share three songs (Gym Hero, Fiesta de Fuego, Sunrise City), because both want loud, non-acoustic songs with singing. Gym Hero is #2 for both, but for different reasons: for pop it matches the genre, and for rock it matches the "intense" mood. Only the genre and mood are different, so it makes sense that the rest of the list is similar.
- **Deep Intense Rock vs. Sad but Hyped:** Both want energy 0.90, so spots #2 to #5 are almost the same loud songs. The only difference is #1: Sad but Hyped gets Letters I Never Sent, a *calm* sad folk song. Matching genre and mood (3 points) beat being far off on energy (it only lost 0.66), so the system picked "sad" over "hyped."
- **Deep Intense Rock vs. Acoustic Headbanger:** Both want really loud music, but the rock list stays loud the whole way down, while the headbanger list fills #3 to #5 with calm lofi and jazz. The only change is asking for acoustic and no singing, and in my data those songs are all calm, so the +1.0 in bonuses outweighed the energy gap. This doesn't really make sense for the user, and it's how I found the main weakness in section 6.
- **Pop / Happy vs. Capital Letters:** These should give the same results, but they don't. The capital letters made genre and mood never match, so the list turned into "songs sorted by energy." This shows the matching is too strict.
- **Pop / Happy vs. Not in Catalog:** Pop / Happy's #1 scores 4.98 with a big gap to the rest. Not in Catalog's top 5 are all squeezed between 1.85 and 1.94, which basically means "nothing matched, here's some medium-high energy songs." The system still recommends things without telling the user nothing really fit.
- **Deep Intense Rock vs. Energy Too High:** Both lists rank the loudest songs near the top, which is the right idea. But no song can ever be "close" to 1.5, so the energy points are much lower, and the quietest songs actually get negative points. The order makes sense, but the scores don't.

**Experiment: weight shift**

I tried cutting the genre weight in half (2.0 to 1.0) and doubling the energy weight (1.0 to 2.0). The best possible score stayed at 5.0, so the math still worked. Six of the eight profiles kept the exact same order, and only the numbers changed. Two got a little better: Pop / Happy moved Rooftop Lights (happy) above Gym Hero (intense), and Acoustic Headbanger stopped getting study music. But Iron Tempest still ranked behind Fiesta de Fuego for the rock fan, because the real problem is that "metal" doesn't count as "rock," and weights can't fix that. Since it was mostly just different and not more accurate, I went back to the original weights.

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
