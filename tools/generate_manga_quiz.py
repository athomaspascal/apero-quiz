import json
import uuid
from datetime import datetime

# Fonction pour générer un UUID unique
def generate_uuid():
    return str(uuid.uuid4())

# Données des mangas célèbres
manga_data = [
    # Format: (nom, auteur, personnages, date, nombre_volumes, terminé, thème, type)
    ("One Piece", "Eiichiro Oda", "Monkey D. Luffy, Roronoa Zoro, Nami, Sanji", "1997", "Plus de 100", "Non", "Aventure, Pirates", "Shōnen"),
    ("Naruto", "Masashi Kishimoto", "Naruto Uzumaki, Sasuke Uchiha, Sakura Haruno, Kakashi Hatake", "1999", "72", "Oui", "Ninja, Action", "Shōnen"),
    ("Dragon Ball", "Akira Toriyama", "Son Goku, Vegeta, Bulma, Piccolo", "1984", "42", "Oui", "Arts martiaux, Aventure", "Shōnen"),
    ("Attack on Titan", "Hajime Isayama", "Eren Yeager, Mikasa Ackerman, Armin Arlert", "2009", "34", "Oui", "Action, Dark Fantasy", "Shōnen"),
    ("Death Note", "Tsugumi Ohba", "Light Yagami, L, Ryuk, Misa Amane", "2003", "12", "Oui", "Thriller, Surnaturel", "Shōnen"),
    ("My Hero Academia", "Kohei Horikoshi", "Izuku Midoriya, Katsuki Bakugo, Ochaco Uraraka", "2014", "Plus de 35", "Non", "Super-héros, Action", "Shōnen"),
    ("Demon Slayer", "Koyoharu Gotouge", "Tanjiro Kamado, Nezuko Kamado, Zenitsu Agatsuma", "2016", "23", "Oui", "Action, Surnaturel", "Shōnen"),
    ("Fullmetal Alchemist", "Hiromu Arakawa", "Edward Elric, Alphonse Elric, Roy Mustang", "2001", "27", "Oui", "Alchimie, Aventure", "Shōnen"),
    ("Bleach", "Tite Kubo", "Ichigo Kurosaki, Rukia Kuchiki, Orihime Inoue", "2001", "74", "Oui", "Action, Surnaturel", "Shōnen"),
    ("Hunter x Hunter", "Yoshihiro Togashi", "Gon Freecss, Killua Zoldyck, Kurapika, Leorio", "1998", "Plus de 36", "Non", "Aventure, Action", "Shōnen"),
    ("Tokyo Ghoul", "Sui Ishida", "Ken Kaneki, Touka Kirishima, Hideyoshi Nagachika", "2011", "14", "Oui", "Dark Fantasy, Horreur", "Seinen"),
    ("One Punch Man", "ONE", "Saitama, Genos, Mumen Rider", "2009", "Plus de 28", "Non", "Super-héros, Comédie", "Seinen"),
    ("Sailor Moon", "Naoko Takeuchi", "Usagi Tsukino, Ami Mizuno, Rei Hino", "1991", "18", "Oui", "Magical Girl, Romance", "Shōjo"),
    ("Berserk", "Kentaro Miura", "Guts, Griffith, Casca", "1989", "41", "Non (décès de l'auteur)", "Dark Fantasy, Action", "Seinen"),
    ("JoJo's Bizarre Adventure", "Hirohiko Araki", "Jonathan Joestar, Joseph Joestar, Jotaro Kujo", "1987", "Plus de 130", "Non", "Aventure, Surnaturel", "Shōnen"),
    ("Fairy Tail", "Hiro Mashima", "Natsu Dragneel, Lucy Heartfilia, Erza Scarlet", "2006", "63", "Oui", "Magie, Aventure", "Shōnen"),
    ("Sword Art Online", "Reki Kawahara", "Kirito, Asuna, Klein", "2009", "Plus de 25", "Non", "VRMMORPG, Romance", "Light Novel adapté"),
    ("Tokyo Revengers", "Ken Wakui", "Takemichi Hanagaki, Manjiro Sano, Ken Ryuguji", "2017", "31", "Oui", "Gang, Voyage dans le temps", "Shōnen"),
    ("Black Clover", "Yūki Tabata", "Asta, Yuno, Noelle Silva", "2015", "Plus de 35", "Non", "Magie, Action", "Shōnen"),
    ("The Promised Neverland", "Kaiu Shirai", "Emma, Norman, Ray", "2016", "20", "Oui", "Thriller, Science-fiction", "Shōnen"),
    ("Chainsaw Man", "Tatsuki Fujimoto", "Denji, Power, Makima", "2018", "11", "Oui", "Action, Horreur", "Shōnen"),
    ("Spy x Family", "Tatsuya Endo", "Loid Forger, Yor Forger, Anya Forger", "2019", "Plus de 12", "Non", "Comédie, Espionnage", "Shōnen"),
    ("Haikyuu!!", "Haruichi Furudate", "Shoyo Hinata, Tobio Kageyama", "2012", "45", "Oui", "Sport, Volley-ball", "Shōnen"),
    ("Slam Dunk", "Takehiko Inoue", "Hanamichi Sakuragi, Kaede Rukawa", "1990", "31", "Oui", "Sport, Basket-ball", "Shōnen"),
    ("Yu Yu Hakusho", "Yoshihiro Togashi", "Yusuke Urameshi, Kazuma Kuwabara, Kurama, Hiei", "1990", "19", "Oui", "Action, Surnaturel", "Shōnen"),
    ("Rurouni Kenshin", "Nobuhiro Watsuki", "Kenshin Himura, Kaoru Kamiya, Sanosuke Sagara", "1994", "28", "Oui", "Samouraï, Historique", "Shōnen"),
    ("Inuyasha", "Rumiko Takahashi", "Inuyasha, Kagome Higurashi, Miroku, Sango", "1996", "56", "Oui", "Fantasy, Romance", "Shōnen"),
    ("Code Geass", "Ichirō Ōkouchi", "Lelouch Lamperouge, Suzaku Kururugi, C.C.", "2006", "8", "Oui", "Mecha, Stratégie", "Manga adapté d'anime"),
    ("Neon Genesis Evangelion", "Yoshiyuki Sadamoto", "Shinji Ikari, Rei Ayanami, Asuka Langley", "1994", "14", "Oui", "Mecha, Psychologique", "Manga adapté d'anime"),
    ("Cowboy Bebop", "Hajime Yatate", "Spike Spiegel, Jet Black, Faye Valentine", "1998", "3", "Oui", "Science-fiction, Western spatial", "Manga adapté d'anime"),
    ("Vinland Saga", "Makoto Yukimura", "Thorfinn, Askeladd, Canute", "2005", "Plus de 26", "Non", "Vikings, Historique", "Seinen"),
    ("Monster", "Naoki Urasawa", "Kenzo Tenma, Johan Liebert", "1994", "18", "Oui", "Thriller, Psychologique", "Seinen"),
    ("Vagabond", "Takehiko Inoue", "Musashi Miyamoto, Kojiro Sasaki", "1998", "37", "Non", "Samouraï, Historique", "Seinen"),
    ("Boku no Hero Academia", "Kohei Horikoshi", "Izuku Midoriya, All Might, Shoto Todoroki", "2014", "Plus de 37", "Non", "Super-héros, École", "Shōnen"),
    ("Fruits Basket", "Natsuki Takaya", "Tohru Honda, Yuki Sohma, Kyo Sohma", "1998", "23", "Oui", "Romance, Comédie dramatique", "Shōjo"),
    ("Ouran High School Host Club", "Bisco Hatori", "Haruhi Fujioka, Tamaki Suoh", "2002", "18", "Oui", "Comédie, Romance", "Shōjo"),
    ("Cardcaptor Sakura", "CLAMP", "Sakura Kinomoto, Syaoran Li, Tomoyo Daidouji", "1996", "12", "Oui", "Magical Girl, Aventure", "Shōjo"),
    ("Akira", "Katsuhiro Otomo", "Kaneda, Tetsuo", "1982", "6", "Oui", "Cyberpunk, Science-fiction", "Seinen"),
    ("Ghost in the Shell", "Masamune Shirow", "Motoko Kusanagi, Batou", "1989", "3", "Oui", "Cyberpunk, Science-fiction", "Seinen"),
    ("Steins;Gate", "Yomi Sarachi", "Rintaro Okabe, Kurisu Makise", "2009", "3", "Oui", "Science-fiction, Voyage dans le temps", "Manga adapté de visual novel"),
    ("Elfen Lied", "Lynn Okamoto", "Lucy, Kouta, Yuka", "2002", "12", "Oui", "Horreur, Romance", "Seinen"),
    ("Parasyte", "Hitoshi Iwaaki", "Shinichi Izumi, Migi", "1988", "10", "Oui", "Horreur, Science-fiction", "Seinen"),
    ("Blue Exorcist", "Kazue Kato", "Rin Okumura, Yukio Okumura", "2009", "Plus de 28", "Non", "Exorcisme, Surnaturel", "Shōnen"),
    ("D.Gray-man", "Katsura Hoshino", "Allen Walker, Lenalee Lee, Lavi", "2004", "Plus de 27", "Non", "Action, Surnaturel", "Shōnen"),
    ("Magi: The Labyrinth of Magic", "Shinobu Ohtaka", "Aladdin, Alibaba Saluja, Morgiana", "2009", "37", "Oui", "Aventure, Fantasy", "Shōnen"),
    ("Soul Eater", "Atsushi Ohkubo", "Maka Albarn, Soul Eater Evans, Death the Kid", "2004", "25", "Oui", "Action, Surnaturel", "Shōnen"),
    ("Fire Force", "Atsushi Ohkubo", "Shinra Kusakabe, Arthur Boyle, Maki Oze", "2015", "34", "Oui", "Action, Surnaturel", "Shōnen"),
    ("Assassination Classroom", "Yusei Matsui", "Koro-sensei, Nagisa Shiota, Karma Akabane", "2012", "21", "Oui", "Comédie, Action", "Shōnen"),
    ("Food Wars!", "Yuto Tsukuda", "Soma Yukihira, Erina Nakiri", "2012", "36", "Oui", "Cuisine, École", "Shōnen"),
    ("Dr. Stone", "Riichiro Inagaki", "Senku Ishigami, Taiju Oki, Yuzuriha Ogawa", "2017", "26", "Oui", "Science-fiction, Aventure", "Shōnen"),
    ("The Seven Deadly Sins", "Nakaba Suzuki", "Meliodas, Elizabeth Liones, Ban", "2012", "41", "Oui", "Fantasy, Aventure", "Shōnen"),
    ("Noragami", "Adachitoka", "Yato, Hiyori Iki, Yukine", "2011", "Plus de 25", "Non", "Action, Surnaturel", "Shōnen"),
    ("Blue Lock", "Muneyuki Kaneshiro", "Yoichi Isagi, Meguru Bachira", "2018", "Plus de 25", "Non", "Sport, Football", "Shōnen"),
    ("Mob Psycho 100", "ONE", "Shigeo Kageyama, Reigen Arataka", "2012", "16", "Oui", "Action, Comédie", "Seinen"),
    ("Dorohedoro", "Q Hayashida", "Caiman, Nikaido", "2000", "23", "Oui", "Dark Fantasy, Comédie", "Seinen"),
    ("Trigun", "Yasuhiro Nightow", "Vash the Stampede, Meryl Stryfe", "1995", "3", "Oui", "Western spatial, Science-fiction", "Seinen"),
    ("Claymore", "Norihiro Yagi", "Clare, Raki, Teresa", "2001", "27", "Oui", "Dark Fantasy, Action", "Shōnen"),
    ("Black Butler", "Yana Toboso", "Ciel Phantomhive, Sebastian Michaelis", "2006", "Plus de 32", "Non", "Dark Fantasy, Mystère", "Shōnen"),
    ("Pandora Hearts", "Jun Mochizuki", "Oz Vessalius, Alice, Gilbert Nightray", "2006", "24", "Oui", "Fantasy, Mystère", "Shōnen"),
    ("Maid Sama!", "Hiro Fujiwara", "Misaki Ayuzawa, Takumi Usui", "2005", "18", "Oui", "Romance, Comédie", "Shōjo"),
    ("Kamisama Kiss", "Julietta Suzuki", "Nanami Momozono, Tomoe", "2008", "25", "Oui", "Romance, Surnaturel", "Shōjo"),
    ("Skip Beat!", "Yoshiki Nakamura", "Kyoko Mogami, Ren Tsuruga", "2002", "Plus de 48", "Non", "Romance, Comédie", "Shōjo"),
    ("Nana", "Ai Yazawa", "Nana Osaki, Nana Komatsu", "2000", "21", "Non (hiatus)", "Romance, Drame", "Shōjo"),
    ("Paradise Kiss", "Ai Yazawa", "Yukari Hayasaka, George Koizumi", "1999", "5", "Oui", "Romance, Mode", "Josei"),
    ("Lovely Complex", "Aya Nakahara", "Risa Koizumi, Atsushi Otani", "2001", "17", "Oui", "Romance, Comédie", "Shōjo"),
    ("Yona of the Dawn", "Mizuho Kusanagi", "Yona, Hak, Four Dragon Warriors", "2009", "Plus de 40", "Non", "Aventure, Romance", "Shōjo"),
    ("Kaguya-sama: Love Is War", "Aka Akasaka", "Kaguya Shinomiya, Miyuki Shirogane", "2015", "28", "Oui", "Romance, Comédie", "Seinen"),
    ("Horimiya", "HERO", "Kyoko Hori, Izumi Miyamura", "2011", "16", "Oui", "Romance, Slice of Life", "Shōnen"),
    ("Toradora!", "Yuyuko Takemiya", "Ryuji Takasu, Taiga Aisaka", "2006", "10", "Oui", "Romance, Comédie", "Light Novel adapté"),
    ("Re:Zero", "Tappei Nagatsuki", "Subaru Natsuki, Emilia, Rem", "2014", "Plus de 25", "Non", "Fantasy, Psychological", "Light Novel adapté"),
    ("Overlord", "Kugane Maruyama", "Ainz Ooal Gown, Albedo, Shalltear", "2012", "Plus de 15", "Non", "Fantasy, Isekai", "Light Novel adapté"),
    ("No Game No Life", "Yuu Kamiya", "Sora, Shiro", "2012", "Plus de 12", "Non", "Fantasy, Jeux", "Light Novel adapté"),
    ("Mushoku Tensei", "Rifujin na Magonote", "Rudeus Greyrat, Roxy Migurdia", "2014", "Plus de 25", "Non", "Fantasy, Isekai", "Light Novel adapté"),
    ("Goblin Slayer", "Kumo Kagyu", "Goblin Slayer, Priestess", "2016", "Plus de 12", "Non", "Dark Fantasy, Action", "Light Novel adapté"),
    ("That Time I Got Reincarnated as a Slime", "Fuse", "Rimuru Tempest, Shizu", "2015", "Plus de 22", "Non", "Fantasy, Isekai", "Light Novel adapté"),
    ("The Rising of the Shield Hero", "Aneko Yusagi", "Naofumi Iwatani, Raphtalia, Filo", "2014", "Plus de 22", "Non", "Fantasy, Isekai", "Light Novel adapté"),
    ("Konosuba", "Natsume Akatsuki", "Kazuma Satou, Aqua, Megumin, Darkness", "2015", "Plus de 17", "Non", "Fantasy, Comédie", "Light Novel adapté"),
    ("Made in Abyss", "Akihito Tsukushi", "Riko, Reg, Nanachi", "2012", "Plus de 11", "Non", "Aventure, Dark Fantasy", "Seinen"),
    ("Land of the Lustrous", "Haruko Ichikawa", "Phosphophyllite, Cinnabar", "2012", "12", "Oui", "Science-fiction, Fantasy", "Seinen"),
    ("Beastars", "Paru Itagaki", "Legoshi, Haru, Louis", "2016", "22", "Oui", "Drame, Romance", "Shōnen"),
    ("Ranking of Kings", "Sosuke Toka", "Bojji, Kage", "2017", "Plus de 15", "Non", "Fantasy, Aventure", "Web manga"),
    ("The Ancient Magus' Bride", "Kore Yamazaki", "Chise Hatori, Elias Ainsworth", "2013", "Plus de 18", "Non", "Fantasy, Romance", "Shōnen"),
    ("March Comes in Like a Lion", "Chica Umino", "Rei Kiriyama, Akari Kawamoto", "2007", "Plus de 17", "Non", "Drame, Shogi", "Seinen"),
    ("A Silent Voice", "Yoshitoki Oima", "Shoya Ishida, Shoko Nishimiya", "2013", "7", "Oui", "Drame, Romance", "Shōnen"),
    ("Your Lie in April", "Naoshi Arakawa", "Kosei Arima, Kaori Miyazono", "2011", "11", "Oui", "Romance, Musique", "Shōnen"),
    ("Clannad", "Key", "Tomoya Okazaki, Nagisa Furukawa", "2007", "8", "Oui", "Romance, Drame", "Manga adapté de visual novel"),
    ("Anohana", "Mari Okada", "Jinta Yadomi, Meiko Honma", "2012", "3", "Oui", "Drame, Surnaturel", "Manga adapté d'anime"),
    ("Orange", "Ichigo Takano", "Naho Takamiya, Kakeru Naruse", "2012", "6", "Oui", "Romance, Science-fiction", "Shōjo"),
    ("Erased", "Kei Sanbe", "Satoru Fujinuma, Kayo Hinazuki", "2012", "9", "Oui", "Thriller, Mystère", "Seinen"),
    ("Monster Musume", "Okayado", "Kimihito Kurusu, Miia, Papi", "2012", "Plus de 18", "Non", "Comédie, Harem", "Seinen"),
    ("To Love-Ru", "Kentaro Yabuki", "Rito Yuuki, Lala Satalin Deviluke", "2006", "18", "Oui", "Comédie, Harem", "Shōnen"),
    ("High School DxD", "Ichiei Ishibumi", "Issei Hyodo, Rias Gremory", "2008", "Plus de 25", "Non", "Action, Harem", "Light Novel adapté"),
    ("Rosario + Vampire", "Akihisa Ikeda", "Tsukune Aono, Moka Akashiya", "2004", "24", "Oui", "Comédie, Surnaturel", "Shōnen"),
    ("World Trigger", "Daisuke Ashihara", "Yuma Kuga, Osamu Mikumo", "2013", "Plus de 26", "Non", "Science-fiction, Action", "Shōnen"),
    ("Jujutsu Kaisen", "Gege Akutami", "Yuji Itadori, Megumi Fushiguro, Nobara Kugisaki", "2018", "Plus de 24", "Non", "Action, Surnaturel", "Shōnen"),
]

# Créer les questions
questions = []
question_id = 1

# Questions sur l'auteur
for manga_name, author, characters, date, volumes, finished, theme, manga_type in manga_data:
    # Question 1: Qui est l'auteur ?
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Qui est l'auteur du manga '{manga_name}' ?",
        "difficulty_level": 2,
        "options": [author, "Masashi Kishimoto", "Eiichiro Oda", "Akira Toriyama"] if author not in ["Masashi Kishimoto", "Eiichiro Oda", "Akira Toriyama"] else [author, "Hajime Isayama", "Tite Kubo", "Yoshihiro Togashi"],
        "answer": author
    })
    question_id += 1

    # Question 2: Personnages principaux
    main_char = characters.split(",")[0].strip()
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Qui est le personnage principal de '{manga_name}' ?",
        "difficulty_level": 1,
        "options": [main_char, "Naruto Uzumaki", "Monkey D. Luffy", "Ichigo Kurosaki"] if main_char not in ["Naruto Uzumaki", "Monkey D. Luffy", "Ichigo Kurosaki"] else [main_char, "Light Yagami", "Edward Elric", "Gon Freecss"],
        "answer": main_char
    })
    question_id += 1

    # Question 3: Date de première publication
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"En quelle année le manga '{manga_name}' a-t-il été publié pour la première fois ?",
        "difficulty_level": 3,
        "options": [date, "1995", "2000", "2010"] if date not in ["1995", "2000", "2010"] else [date, "1998", "2005", "2015"],
        "answer": date
    })
    question_id += 1

    # Question 4: Nombre de volumes
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Combien de volumes compte le manga '{manga_name}' ?",
        "difficulty_level": 3,
        "options": [volumes, "10", "25", "50"] if volumes not in ["10", "25", "50"] else [volumes, "15", "30", "60"],
        "answer": volumes
    })
    question_id += 1

    # Question 5: Série terminée
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"La série manga '{manga_name}' est-elle terminée ?",
        "difficulty_level": 2,
        "options": [finished, "Oui" if finished == "Non" else "Non"],
        "answer": finished
    })
    question_id += 1

    # Question 6: Thème du manga
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Quel est le thème principal du manga '{manga_name}' ?",
        "difficulty_level": 2,
        "options": [theme, "Romance, Comédie", "Action, Aventure", "Thriller, Mystère"] if theme not in ["Romance, Comédie", "Action, Aventure", "Thriller, Mystère"] else [theme, "Sport, École", "Fantasy, Magie", "Science-fiction, Mecha"],
        "answer": theme
    })
    question_id += 1

    # Question 7: Type de manga
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Quel est le type du manga '{manga_name}' ?",
        "difficulty_level": 2,
        "options": [manga_type, "Shōnen", "Seinen", "Shōjo"] if manga_type not in ["Shōnen", "Seinen", "Shōjo"] else [manga_type, "Josei", "Kodomo", "Light Novel adapté"],
        "answer": manga_type
    })
    question_id += 1

    # Question 8: Personnage secondaire
    if "," in characters:
        second_char = characters.split(",")[1].strip()
        questions.append({
            "id": question_id,
            "uuid": generate_uuid(),
            "question": f"Parmi ces personnages, lequel fait partie du manga '{manga_name}' ?",
            "difficulty_level": 2,
            "options": [second_char, "Sasuke Uchiha", "Vegeta", "L Lawliet"] if second_char not in ["Sasuke Uchiha", "Vegeta", "L Lawliet"] else [second_char, "Rukia Kuchiki", "Sakura Haruno", "Killua Zoldyck"],
            "answer": second_char
        })
        question_id += 1

    # Question 9: Combinaison auteur-manga
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Quel manga a été créé par {author} ?",
        "difficulty_level": 2,
        "options": [manga_name, "Naruto", "One Piece", "Bleach"] if manga_name not in ["Naruto", "One Piece", "Bleach"] else [manga_name, "Death Note", "Attack on Titan", "Dragon Ball"],
        "answer": manga_name
    })
    question_id += 1

    # Question 10: Thème et type combinés
    questions.append({
        "id": question_id,
        "uuid": generate_uuid(),
        "question": f"Le manga '{manga_name}' est de type '{manga_type}'. Quel est son thème ?",
        "difficulty_level": 3,
        "options": [theme, "Romance, École", "Mecha, Science-fiction", "Horreur, Gore"] if theme not in ["Romance, École", "Mecha, Science-fiction", "Horreur, Gore"] else [theme, "Cuisine, Compétition", "Isekai, Fantasy", "Vampire, Surnaturel"],
        "answer": theme
    })
    question_id += 1

# Ajouter des questions générales et variantes pour atteindre 1000
additional_questions = []
q_id = question_id

# Questions sur les genres
genres = ["Shōnen", "Seinen", "Shōjo", "Josei"]
for genre in genres:
    mangas_of_genre = [m[0] for m in manga_data if m[7] == genre]
    if len(mangas_of_genre) >= 4:
        for i in range(min(10, len(mangas_of_genre))):
            manga = mangas_of_genre[i]
            other_mangas = [m for m in mangas_of_genre[:4] if m != manga]
            if len(other_mangas) >= 3:
                additional_questions.append({
                    "id": q_id,
                    "uuid": generate_uuid(),
                    "question": f"Quel manga fait partie du genre {genre} ?",
                    "difficulty_level": 2,
                    "options": [manga] + other_mangas[:3],
                    "answer": manga
                })
                q_id += 1

# Questions sur les années de publication
decades = {
    "1980": [m for m in manga_data if m[3].startswith("198")],
    "1990": [m for m in manga_data if m[3].startswith("199")],
    "2000": [m for m in manga_data if m[3].startswith("200")],
    "2010": [m for m in manga_data if m[3].startswith("201") or m[3].startswith("202")],
}

for decade, mangas in decades.items():
    for manga_info in mangas[:15]:
        manga_name = manga_info[0]
        date = manga_info[3]
        additional_questions.append({
            "id": q_id,
            "uuid": generate_uuid(),
            "question": f"Dans quelle décennie le manga '{manga_name}' a-t-il été publié ?",
            "difficulty_level": 2,
            "options": [f"Années {decade}", "Années 1990", "Années 2000", "Années 2010"] if decade != "1990" else [f"Années {decade}", "Années 1980", "Années 2000", "Années 2010"],
            "answer": f"Années {decade}"
        })
        q_id += 1

# Questions sur les thèmes
themes = list(set([m[6] for m in manga_data]))
for theme in themes[:20]:
    mangas_with_theme = [m for m in manga_data if m[6] == theme]
    if len(mangas_with_theme) >= 2:
        for manga_info in mangas_with_theme[:5]:
            manga_name = manga_info[0]
            additional_questions.append({
                "id": q_id,
                "uuid": generate_uuid(),
                "question": f"Quel est le thème du manga '{manga_name}' ?",
                "difficulty_level": 2,
                "options": [theme, "Romance, Comédie", "Action, Aventure", "Horreur, Mystère"] if theme not in ["Romance, Comédie", "Action, Aventure", "Horreur, Mystère"] else [theme, "Sport, Compétition", "Fantasy, Magie", "Cyberpunk, Futur"],
                "answer": theme
            })
            q_id += 1

# Questions sur les séries terminées vs en cours
finished_mangas = [m for m in manga_data if m[5] == "Oui"]
ongoing_mangas = [m for m in manga_data if m[5] == "Non"]

for manga_info in finished_mangas[:30]:
    manga_name = manga_info[0]
    additional_questions.append({
        "id": q_id,
        "uuid": generate_uuid(),
        "question": f"Le manga '{manga_name}' est-il terminé ?",
        "difficulty_level": 1,
        "options": ["Oui", "Non"],
        "answer": "Oui"
    })
    q_id += 1

for manga_info in ongoing_mangas[:30]:
    manga_name = manga_info[0]
    additional_questions.append({
        "id": q_id,
        "uuid": generate_uuid(),
        "question": f"Le manga '{manga_name}' est-il toujours en cours de publication ?",
        "difficulty_level": 1,
        "options": ["Oui", "Non"],
        "answer": "Oui" if manga_info[5] == "Non" else "Non"
    })
    q_id += 1

# Ajouter questions sur matchmaking auteur-personnage
for manga_info in manga_data[:50]:
    manga_name, author, characters, _, _, _, _, _ = manga_info
    main_char = characters.split(",")[0].strip()
    additional_questions.append({
        "id": q_id,
        "uuid": generate_uuid(),
        "question": f"Qui a créé le personnage '{main_char}' ?",
        "difficulty_level": 3,
        "options": [author, "Masashi Kishimoto", "Eiichiro Oda", "Hajime Isayama"] if author not in ["Masashi Kishimoto", "Eiichiro Oda", "Hajime Isayama"] else [author, "Akira Toriyama", "Tite Kubo", "ONE"],
        "answer": author
    })
    q_id += 1

# Questions sur les types Light Novel adaptés
light_novel_mangas = [m for m in manga_data if "Light Novel" in m[7]]
for manga_info in light_novel_mangas:
    manga_name = manga_info[0]
    additional_questions.append({
        "id": q_id,
        "uuid": generate_uuid(),
        "question": f"Le manga '{manga_name}' est-il adapté d'un light novel ?",
        "difficulty_level": 2,
        "options": ["Oui", "Non"],
        "answer": "Oui"
    })
    q_id += 1

    additional_questions.append({
        "id": q_id,
        "uuid": generate_uuid(),
        "question": f"Quel est le type d'origine du manga '{manga_name}' ?",
        "difficulty_level": 2,
        "options": ["Light Novel adapté", "Manga original", "Anime adapté", "Visual Novel adapté"],
        "answer": "Light Novel adapté"
    })
    q_id += 1

# Combiner toutes les questions
all_questions = questions + additional_questions

# Limiter à 1000 questions
all_questions = all_questions[:1000]

# Créer le quiz
manga_quiz = {
    "name": "Famous Manga Series",
    "imageFileName": "manga.svg",
    "questions": all_questions
}

# Sauvegarder dans un fichier temporaire
with open(r'C:\Users\athom\IdeaProjects\quizz1\manga_quiz_temp.json', 'w', encoding='utf-8') as f:
    json.dump(manga_quiz, f, ensure_ascii=False, indent=2)

print(f"Quiz manga généré avec {len(all_questions)} questions!")
print(f"Sauvegardé dans manga_quiz_temp.json")

