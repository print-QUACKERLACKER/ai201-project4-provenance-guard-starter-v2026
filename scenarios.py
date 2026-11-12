"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "AI paragraphs",
        "criterion": 1,
        # Target: at least 8 of 10 labelled AI. Written by Claude (an AI
        # chatbot) when asked for a paragraph on each everyday topic.
        "texts": [
            "Cats make wonderful pets for people with busy lifestyles. They are independent, clean, and able to entertain themselves for hours while their owners are at work. At the same time, they form strong bonds with the people they live with and often show affection in subtle but meaningful ways. For many households, a cat offers the perfect balance of companionship and low maintenance.",
            "Reading books offers numerous benefits for both the mind and overall well-being. It improves vocabulary, strengthens concentration, and exposes readers to new ideas and perspectives. Fiction in particular can help people develop empathy by allowing them to experience the world through the eyes of different characters. Whether it is a novel, a biography, or a self-help guide, reading remains one of the most valuable habits a person can build.",
            "Regular exercise plays a crucial role in maintaining good physical and mental health. It strengthens the heart, improves flexibility, and helps people maintain a healthy weight. In addition, physical activity releases endorphins, which can reduce stress and improve mood. Even small amounts of daily movement, such as a brisk walk, can make a significant difference over time.",
            "Summer is a favorite season for many people because of its warm weather and long, sunny days. It provides the perfect opportunity for outdoor activities such as swimming, hiking, and spending time at the beach. Many families also take vacations during the summer, creating lasting memories together. The relaxed pace of the season allows people to recharge and enjoy life to the fullest.",
            "Learning a second language can open up a world of new opportunities. It allows people to communicate with others from different cultures and gain a deeper understanding of how they live. Bilingual individuals often have an advantage in the job market, as many employers value language skills. Furthermore, studies suggest that learning a new language can improve memory and problem-solving abilities.",
            "Technology has transformed the way people communicate with one another. Smartphones, social media, and video calls make it possible to stay connected with friends and family no matter where they are in the world. While these tools offer incredible convenience, they also raise important questions about privacy and screen time. Finding a healthy balance is essential to making the most of modern communication.",
            "Cooking at home offers a variety of benefits that go beyond simply saving money. It gives people full control over the ingredients they use, making it easier to prepare healthy and nutritious meals. Cooking can also be a creative and relaxing activity that brings family members together. Over time, developing cooking skills can boost confidence and encourage a more mindful approach to eating.",
            "Spending time in nature has a powerful positive effect on mental health. Activities such as walking in a park, hiking through a forest, or sitting by a lake can help reduce stress and anxiety. Being surrounded by greenery and fresh air encourages people to slow down and appreciate the present moment. As a result, many experts recommend making time for nature as part of a balanced lifestyle.",
            "Music is a universal language that connects people across cultures and generations. It has the ability to evoke strong emotions, bring back memories, and lift people's spirits during difficult times. Many people also use music to help them focus while studying or working. Whether it is classical, pop, or jazz, music plays an important role in the lives of people all around the world.",
            "Volunteering is a meaningful way to give back to the community while also gaining valuable experience. It allows individuals to develop new skills, meet like-minded people, and make a real difference in the lives of others. Many volunteers report feeling a greater sense of purpose and fulfillment as a result of their work. Ultimately, volunteering benefits both the people being helped and the volunteers themselves.",
        ],
    },
    {
        "name": "my stiff writing",
        "criterion": 2,
        # Target: at most 2 of 5 labelled AI. YOUR OWN writing, in the
        # structured "Firstly... Second... Lastly" school style. At least
        # 3 sentences and 40 words each.
        "texts": [
            # All five are the paragraphs of my own old school essay on social media
            # and the Health Triangle, pasted whole and unedited. It's the taught
            # intro / Firstly / Secondly / solution / Overall structure. The body
            # paragraphs quote two articles ("Meet Facebook's Mr. Nice", "The Secret
            # Social Media Lives of Teenagers"), so a few sentences are a
            # journalist's, not mine; both are human-written.
            'Social media, it’s the platform media-wise that you’re mostly on every single day. Many people use social media differently, and have different goals. Wanting to make new friendships, looking up information, checking the news, it’s all there. However, what people don’t recognize is the fact that there are both positive and negative sides to usage of social media. Both these positives and negatives can impact us, or rather, our health in many ways. Mentally, physically and socially, social media has an effect on all these components, which are part of our Health Triangle, the thing we try to maintain on a daily basis. This brings the question, how can social media impact us positively and negatively, and what can we do about it?',
            "Firstly, the positive effects of using social media. Social media and the internet in general makes it extremely quick for us to obtain information. You wouldn’t have to go asking around or searching physically for this knowledge, but instead can do a quick search online. Positively speaking, this feature can strengthen our mental health. There are multiple resources online for us to check on trustworthy information. Helpful study mechanisms also help to improve our thinking and understanding processes. An example of this would be if you have an upcoming test and not many resources are provided. You’re stuck on how one thing works in your study, but luckily, you have the internet. One search leads to many, many resources that can help you. By having this new information, you’re able to strengthen your brain/mental state since now, you probably know all the materials and are more confident. This could also affect other people’s mental health, if you were to share this newly obtained information with them. In addition to this, social media is also a way to create new friendships. The whole idea of social media is to meet new people, express your interests and such online. This benefits your social part of the health triangle. Although you’re not actually interacting with them, you’re able to talk to these strangers who may soon become friends with you, and that could lead to real life interactions. Connecting with others, sharing what you like or dislike, it’s all part of building up your social health. This effect could also impact other people’s social health, since they’re also able to meet you as a new person, expanding their social connections. Another positive effect is maintaining safety. On almost all social media, there are moderators, useful pages/ buttons to report inappropriate content and so on. Being able to feel safe on what you post, do or say on social media can really boost someone’s mental health, because feeling safe is what people need to feel when being online. According to “Meet Facebook’s Mr. Nice”, it says “The company told me that each week eight million Facebook members use tools that allow users to report a harmful post or photo.” This proves that many people online are able to contribute to this safety online for all users by doing their share of preventing harmful content to be spread around. And, this also affects people's mental state because with the feeling of safety from one person, it could also cause them to feel safe due to environmental factors.",
            'Secondly, the negative effects of using social media. An obviously huge problem would be cyberbullying. It’s probably something done by people everyday online, but they don’t realize how much of a negative effect that can have on others. Bullying in general is already not a good thing to do, as it’s an action revolving around purposely making fun of someone. In the text, “Meet Facebook’s Mr. Nice”, it states, “Most people I know who have quit services like Twitter and Instagram have done so because commenters were spiteful, insensitive or just plain nasty”, and “According to a report released this week by Pew Research’s Internet Project, 65 percent of young adults 18 to 29 in the United States said that they had been harassed online, and 92 percent had witnessed someone else being bullied.” These quotes indicate that cyberbullying isn’t a minor thing that you could just overlook, it’s something that has a far more greater impact on a large number of people online than you would normally perceive. In cyber bullying, you wouldn’t know the person behind the other side of the screen, therefore, you wouldn’t know how they’re feeling or their mental state because you aren’t able to see them in person. These actions of bullying someone online can have an immense impact on someone else’s mental part of the health triangle. They may soon develop negative thoughts and start doubting themselves due to the pressure and bullying done online. A lot of these negative thoughts and pressure can continue to add on and on because of this cyberbullying, and can create an unstable mindset. And, an unstable mindset can lead to also affecting the social and physical parts of the health triangle, since it’s your mental state that decides what you want to do. An impact on someone’s mental state can also have an effect on the people around them, they try and try to help this mentally injured person, but it’s not something they can see. This would also lead to the other people to be affected mentally, desperately figuring out ways to help an individual. In addition to cyberbullying, it can also get additing. According to the text, The Secret Social Media Lives of Teenagers”, it says “Over time, teens’ own values may become convoluted within an online world of instantaneous feedback, and their behavior online can become based on their “all about the likes” values rather than their real‑life values.” People spend hours and hours on social media daily, limiting their movements because they’re so captivated by what’s online. This could affect your physical health. Instead of maintaining your body and exercising regularly, you’re wasting time online and doing nothing. Less exercise and movement can lead to a worse physical state for people because they’re doing nothing everyday. Less time moving around and exercising can impact family and friends mentally. Since you’re so addicted on social media, you wouldn’t be able to spend time with others and communicate with them. They would think less of you and a loss of connection would probably occur.',
            'Despite the negative factors on social media, there is a way to limit them from happening too much and expanding the benefits of social media. To limit the risks of negativity on social media, it’s simple, just report any risky content so it can be removed immediately. With a simple click, preventing potential risks on social media from spreading will be a simple task. In the text,  “Meet Facebook’s Mr. Nice”, it states “Mr. Bejar’s team designed these tools to let people know someone had hurt their feelings, and he said the system actually worked.” Tools, referring to the report features, shows that with a single press of a button, inappropriate and risky content online can be reduced with the help of social media users, and even you. Less of this harm being spread around, can lead to positive side effects, like a safer environment. With all these harmful posts/ content gone, it can lead to a much more safe platform, which can help many users feel relieved on being able to be on social media without any potential harm.',
            'Overall, social media has its positive effects and potential risks. You can still keep using social media, but be aware of certain content that is presented online. Contributing to the solution of reporting inappropriate and risky content online can lead to positive side effects on your health triangle. Many people don’t often think of how social media plays a role on impacting our health in general, but if you look closely, risks like cyberbullying, addictiveness happen everyday, and they usually have a negative impact on someone’s mental state. Although there are the positive sides of social media like quick searches, a chance to make new friends, safety, etc. we still have to be careful online.',
        ],
    },
    {
        "name": "can't tell",
        "criterion": 3,
        # Target: at least 2 of 5 labelled unsure. Texts YOU honestly can't
        # call either way, e.g. an AI paragraph you've edited by hand, or your
        # own writing with AI-style phrasing mixed in.
        "texts": [
            # Can't-tell 1: my own meditation piece. The opening is my voice, the
            # middle is encyclopedia-style phrasing, so it reads either way.
            'It’s something you’ve definitely seen on television once or twice– an instructor sitting upright, eyes closed and telling you to focus on breathing..? Meditation is something we’re all familiar with, but just how familiar are we with the process from start to finish? I was formally introduced to meditation in highschool, when my gym teacher allocated 5 minutes after an hour long period of work outs. Me and my classmates didn’t take this time seriously, and I would often laugh when I heard that meditation “works.” Contrary to what I thought, meditation is indeed a health practice that is proven to work. “According to the National Health Interview Survey, an annual nationally representative survey, the percentage of U.S. adults who practiced meditation more than doubled between 2002 and 2022, from 7.5 to 17.3 percent.” Derived from Eastern origins, meditation is a technique used in several cultures and practices. One example is Zen meditation, which comes from Buddhist culture that mainly focuses on how you breathe. For Mantra meditation, one focuses on a word, phrase or syllable to guide their meditation. One of the most common meditation techniques you may know is known as yoga meditation that utilizes yoga in order to relieve the nervous system. Meditation today is known to help treat symptoms of depression, anxiety, asthma, heart disease, and even cancer. And what’s more– meditation is a free practice that only requires you and your mind.',
            # Can't-tell 2: AI draft (friendship) written by Claude, then lightly
            # edited by me (a few words and phrases changed).
            'Strong friendships are an important part of a happy and healthy life. Good friends will offer support during difficult times and celebrate with you through the good times. Building these relationships takes effort, including listening, being honest, and making time for one another. In the end, the friends we choose can have a lasting influence on who we become.',
            # Can't-tell 3: AI draft (studying late) written by Claude, then lightly
            # edited by me (a few words and phrases changed).
            'Studying late at night is a habit many do, especially during exam season. Although the silence can make it easier to focus, staying up too late often leads to poor sleep and lower energy the next day. Research suggests that a consistent sleep schedule improves memory and concentration. Planning ahead can help with avoiding the need for last-minute cramming.',
            # Can't-tell 4: AI draft (music) written by Claude, then lightly
            # edited by me (a few words and phrases changed).
            'Many people like listening to music while they study or work. For some, it creates a relaxing atmosphere that makes difficult tasks feel more manageable. Instrumental music in particular can help muffle background noise without being too distracting. However, songs with lyrics might be too distracting.',
            # Can't-tell 5: AI draft (part-time jobs) written by Claude, then lightly
            # edited by me (a few words and phrases changed).
            "Having a part-time job during high school can teach many valuable lessons won't appear in a classroom. Working with customers builds patience and communication skills, while managing a schedule encourages organization and planning. Earning your own money also helps you understand the value of saving or investing. However, it is important to make sure work does not take away from schoolwork or sleep.",
        ],
    },
    {
        "name": "my own writing",
        "criterion": 4,
        # Target: at most 2 of 10 labelled AI. YOUR OWN writing in your
        # normal style. Old school essays and assignments count.
        "texts": [
            # The paragraph from unit 7's calibration.
            "Dogs are my favorite animals for many reasons. Firstly, they're a man's best friend, they will follow you anywhere and smile when you smile. Second, they're extremely adorable when they're puppies. Lastly, I love my own dog very much, so he has taught me to love other dogs aswell!",
            # Paragraphs 2-6: written by me about running, in my normal casual
            # style. Typos left in on purpose; that's how I actually write.
            "i like running since it's a form of exercise-- my parents tell me to do it in the morning for good luck. I just do it because it helps with my cardio. my parents met each other on a run so its been good luck for them and they hope its the same for me",
            "lately, running has been a favorite hobby of mine. i enjoy waking up first thing in the morning and jogging when the sun rises. there is something refreshing about waking up with the sun. the morning is rejuvenating after a long sleep and it gets you ready for the rest of the day. the morning breeze is peaceful",
            "the other day, i saw my crush while she was on the track. she looked really cool, focused on getting her laps in and it honestly inspired me to start running myelf. it's been difficult getting started but i have learned to endure.",
            "one form of exercise i hate is running.. i dont understand how some enjoy it. i believe it does have its health benefits, but after a few seconds of running down the track, i feel my body collaspe and i genuinely cannot take another step.",
            "running is extremely beneficial for people who wish to build endurance and those who focus on cardio. several studies have shown that running helps with both physical and mental health. running has helped me clear my head for my daily activities and also helps me stay awake during mundane periods",
            # Paragraphs 7-10: my own personal narrative essay about getting over
            # my fear of speaking up. Not rubric-structured, so it counts as my
            # normal style. Its paragraphs are short, so it's split into four
            # passages in order, along my own paragraph breaks. Words unchanged.
            'I was a button away. My heart raced to the finish line, as it accelerated faster and faster until my finger hit the ‘join’ button. “Welcome to the Awards Ceremony!” My heart passed the finish line but was still running.\n\nMy heart always stuttered along with my words when I tried to speak. It was embarrassing. I didn’t like it. When middle school arrived it was truly another world. I also learned something new about myself.\n\nI was horrible at socializing and speaking.\n\nEvery time I was called on, my heart pounded in my ears. My voice wasn’t as loud as it used to be, and when it was, it was when I stumbled on my words. I had to change for the future– how else was I going to speak to others?',
            'When the summer after 8th grade arrived, I dreaded the first day of high school. I didn’t want to relive the experience of not being able to speak properly. The thought kept me up each night as time edged closer to the first day of online school. It’s going to be the same, I thought. I don’t want to go through middle school again, I complained.\n\nWait, online school? Online school, I had thought about it for a good while, is way different from being in a classroom.\n\nIt’s true that my heart still pounded in my ears when I was waiting to join the first class, but something was different. I was determined to make a good impression– not the gloomy kid I was in middle school, but the person I was in elementary school. With a simple button, I spoke. I forced the words out, swallowing all my fears since I knew nothing would come out of not trying.',
            'When the words came out of my mouth, I realized I had spoken perfectly fine. There were no stumbles, my heart still raced but not in shame, but success. After that, it was normal for me to speak. I still stuttered or messed up a few words, but there were no bad feelings. Instead, they had been replaced with joy and accomplishments.\n\nAfter I received an email invite to the school awards ceremony, I was surprised. What had I done to get such a great email? After seconds that seemed like hours, my heart was running again. The year was ending, so the finish line was also near. I joined and waited patiently for my name. When it was called, all my senses were focused on the screen.\n\nI won an award for my ability to participate frequently in English class.',
            'It was one of the few times I felt proud of myself. I had gotten up from an obstacle that I thought would pester me for the rest of my life, but with surprise, I was able to knock it down and run forward. I was able to learn more about myself– that I could do something that I considered impossible a few years ago through willpower.\n\nThat feeling of dread– the weight on my shoulders disappeared in an instant from that moment on. Today in my classes and in daily life, I can speak more, connect with others, and understand more because I tackled my fears of speaking. I feel more accomplished and also gained new experiences that I couldn’t have obtained without speaking up. One such experience is making friends– back then, I didn’t have the guts to speak, and that factor was detrimental to my social life as I spoke to just a few people.\n\nHowever, now that’s different. I’m different now. I was able to make a lot of new friends, each amazingly awesome in their own way. With my new power to communicate better, I feel as if I can do anything.\n\nAnd it’s all because of me.',
        ],
    },
    {
        "name": "published human writing",
        "criterion": 5,
        # Target: at most 2 of 10 labelled AI. Paragraphs copied from news
        # articles or essays published before 2022. Five are modern US-government
        # pages (public domain) dated by Wayback Machine snapshots from 2019-2020;
        # five are public-domain essays and memoirs from Project Gutenberg.
        "texts": [
            # National Park Service, Yellowstone 'Wolves' page (nps.gov/yell/learn/nature/wolves.htm), Wayback snapshot 2019-12-15
            'Wolves are highly social animals and live in packs. Worldwide, pack size will depend on the size and abundance of prey. In Yellowstone, average pack size is 10 individuals. The pack is a complex social family, with older members (often the alpha male and alpha female) and subordinates, each having individual personality traits and roles within the pack. Packs defend their territory from other, invading packs by howling and scent marking with urine.',
            # National Park Service, Yellowstone 'Wolves' page, Wayback snapshot 2019-12-15
            'Many other animals benefit from wolf kills. For example, when wolves kill an elk, ravens arrive almost immediately. Coyotes arrive soon after, waiting nearby until the wolves are sated. Bears will attempt to chase the wolves away, and are usually successful. Many other animals—from magpies to invertebrates—consume the remains.',
            # National Weather Service, 'Lightning Science Overview' (weather.gov/safety/lightning-science-overview), Wayback snapshot 2019-08-15
            'Lightning is fascinating to watch but also extremely dangerous. In the United States, there are about 25 million lightning flashes every year. Each of those 25 million flashes is a potential killer. While lightning fatalities have decreased over the past 30 years, lightning continues to be one of the top weather killers in the United States. In addition, lightning injures many more people than it kills and leaves some victims with life-long health problems.',
            # National Weather Service, 'Lightning Science Overview', Wayback snapshot 2019-08-15
            'Thunder is the sound made by a flash of lightning. As lightning passes through the air it heats the air quickly. This causes the air to expand rapidly and creates the sound wave we hear as thunder. Normally, you can hear thunder about 10 miles from a lightning strike. Since lightning can strike outward 10 miles from a thunderstorm, if you hear thunder, you are likely within striking distance from the storm.',
            # US Fish & Wildlife Service, 'Threats to Birds' (fws.gov/birds/bird-enthusiasts/threats-to-birds.php), Wayback snapshot 2020-01-01
            'Both natural and human-caused sources of bird mortality contribute cumulative or combined effects to declining bird populations. Millions of acres of bird habitat are lost or degraded every year due to development, agriculture, and forestry practices. These rapidly accelerating impacts can be mitigated only through habitat restoration and protection. In addition, millions of birds are directly killed by human-caused sources such as collisions with man-made structures. Death from natural causes is also common sources of mortality.',
            # Frederick Douglass, Narrative of the Life of Frederick Douglass (1845), Project Gutenberg #23
            'I was probably between seven and eight years old when I left Colonel Lloyd’s plantation. I left it with joy. I shall never forget the ecstasy with which I received the intelligence that my old master (Anthony) had determined to let me go to Baltimore, to live with Mr. Hugh Auld, brother to my old master’s son-in-law, Captain Thomas Auld. I received this information about three days before my departure. They were three of the happiest days I ever enjoyed. I spent the most part of all these three days in the creek, washing off the plantation scurf, and preparing myself for my departure.',
            # W. E. B. Du Bois, The Souls of Black Folk (1903), Project Gutenberg #408
            'I have sought to paint an average picture of real relations between the sons of master and man in the South. I have not glossed over matters for policy’s sake, for I fear we have already gone too far in that sort of thing. On the other hand, I have sincerely sought to let no unfair exaggerations creep in. I do not doubt that in some Southern communities conditions are better than those I have indicated; while I am no less certain that in other communities they are far worse.',
            # Benjamin Franklin, Autobiography (written 1771-1790), Project Gutenberg #20203
            "The business of the post-office occasion'd my taking a journey this year to New England, where the College of Cambridge, of their own motion, presented me with the degree of Master of Arts. Yale College, in Connecticut, had before made me a similar compliment. Thus, without studying in any college, I came to partake of their honours. They were conferr'd in consideration of my improvements and discoveries in the electric branch of natural philosophy.",
            # John Muir, My First Summer in the Sierra (1911), Project Gutenberg #32540
            'We were pelted about noon by a short, heavy rainstorm, sublime thunder reverberating among the mountains and cañons,—some strokes near, crashing, ringing in the tense crisp air with startling keenness, while the distant peaks loomed gloriously through the cloud fringes and sheets of rain. Now the storm is past, and the fresh washed air is full of the essences of the flower gardens and groves. Winter storms in Yosemite must be glorious. May I see them!',
            # Henry David Thoreau, Walden (1854), Project Gutenberg #205
            'Every man is the builder of a temple, called his body, to the god he worships, after a style purely his own, nor can he get off by hammering marble instead. We are all sculptors and painters, and our material is our own flesh and blood and bones. Any nobleness begins at once to refine a man’s features, any meanness or sensuality to imbrute them.',
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
