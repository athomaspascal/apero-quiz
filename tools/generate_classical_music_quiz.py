import json
import uuid
import sys

# Generate Classical Music Composers Quiz
quiz = {
    "name": "Classical Music Composers",
    "imageFileName": "classical-music.svg",
    "questions": []
}

questions_data = [
    # Mozart questions
    ("What is Wolfgang Amadeus Mozart's birth year?", ["1756", "1770", "1750", "1760"], "1756", 1),
    ("In which city was Mozart born?", ["Salzburg", "Vienna", "Prague", "Munich"], "Salzburg", 1),
    ("What was Mozart's full name?", ["Wolfgang Amadeus Mozart", "Johann Sebastian Mozart", "Ludwig Wolfgang Mozart", "Franz Wolfgang Mozart"], "Wolfgang Amadeus Mozart", 2),
    ("At what age did Mozart compose his first piece?", ["5", "8", "10", "12"], "5", 2),
    ("What year did Mozart die?", ["1791", "1800", "1785", "1795"], "1791", 1),
    ("How many symphonies did Mozart compose?", ["41", "50", "35", "60"], "41", 3),
    ("What is Mozart's most famous opera?", ["The Magic Flute", "Carmen", "La Traviata", "Aida"], "The Magic Flute", 2),
    ("Who was Mozart's main rival in Vienna?", ["Antonio Salieri", "Joseph Haydn", "Ludwig van Beethoven", "Franz Schubert"], "Antonio Salieri", 2),
    ("What was Mozart's Requiem Mass commissioned for?", ["His own funeral", "A wealthy patron", "The Emperor", "A church"], "A wealthy patron", 3),
    ("In which language are most of Mozart's operas?", ["Italian", "German", "French", "Latin"], "Italian", 2),

    # Beethoven questions
    ("What year was Ludwig van Beethoven born?", ["1770", "1756", "1780", "1765"], "1770", 1),
    ("In which city was Beethoven born?", ["Bonn", "Vienna", "Leipzig", "Berlin"], "Bonn", 1),
    ("How many symphonies did Beethoven compose?", ["9", "12", "7", "15"], "9", 1),
    ("Which symphony is known as the 'Choral Symphony'?", ["Symphony No. 9", "Symphony No. 5", "Symphony No. 3", "Symphony No. 6"], "Symphony No. 9", 2),
    ("What major affliction did Beethoven suffer from?", ["Deafness", "Blindness", "Paralysis", "Tuberculosis"], "Deafness", 1),
    ("What is the nickname of Beethoven's Symphony No. 6?", ["Pastoral", "Heroic", "Fate", "Romantic"], "Pastoral", 2),
    ("What year did Beethoven die?", ["1827", "1830", "1820", "1835"], "1827", 1),
    ("Which symphony is dedicated to Napoleon?", ["Symphony No. 3 (Eroica)", "Symphony No. 5", "Symphony No. 9", "Symphony No. 7"], "Symphony No. 3 (Eroica)", 3),
    ("What is Beethoven's only opera?", ["Fidelio", "Don Giovanni", "The Magic Flute", "Carmen"], "Fidelio", 2),
    ("Who was Beethoven's teacher in Vienna?", ["Joseph Haydn", "Antonio Salieri", "Wolfgang Amadeus Mozart", "Franz Schubert"], "Joseph Haydn", 3),

    # Bach questions
    ("What year was Johann Sebastian Bach born?", ["1685", "1700", "1670", "1695"], "1685", 1),
    ("In which country was Bach born?", ["Germany", "Austria", "Italy", "France"], "Germany", 1),
    ("What is Bach's most famous organ work?", ["Toccata and Fugue in D minor", "Air on the G String", "Brandenburg Concertos", "The Well-Tempered Clavier"], "Toccata and Fugue in D minor", 2),
    ("How many Brandenburg Concertos did Bach compose?", ["6", "4", "8", "10"], "6", 2),
    ("What was Bach's primary occupation?", ["Church organist and composer", "Court musician", "Opera composer", "Music teacher"], "Church organist and composer", 2),
    ("What year did Bach die?", ["1750", "1760", "1740", "1755"], "1750", 1),
    ("How many children did Bach have?", ["20", "10", "15", "12"], "20", 3),
    ("What is 'The Well-Tempered Clavier'?", ["A collection of preludes and fugues", "An opera", "A symphony", "A mass"], "A collection of preludes and fugues", 3),
    ("Which Bach work is often played at weddings?", ["Jesu, Joy of Man's Desiring", "Toccata and Fugue", "Brandenburg Concerto No. 3", "Air on the G String"], "Jesu, Joy of Man's Desiring", 2),
    ("In which city did Bach spend most of his career?", ["Leipzig", "Vienna", "Berlin", "Dresden"], "Leipzig", 2),

    # Chopin questions
    ("What year was Frédéric Chopin born?", ["1810", "1820", "1800", "1815"], "1810", 1),
    ("In which country was Chopin born?", ["Poland", "France", "Germany", "Austria"], "Poland", 1),
    ("What instrument was Chopin famous for?", ["Piano", "Violin", "Cello", "Flute"], "Piano", 1),
    ("In which city did Chopin spend most of his adult life?", ["Paris", "Warsaw", "Vienna", "London"], "Paris", 2),
    ("What year did Chopin die?", ["1849", "1850", "1845", "1855"], "1849", 1),
    ("How many piano concertos did Chopin compose?", ["2", "5", "3", "1"], "2", 2),
    ("What is a 'Nocturne'?", ["A night piece", "A dance", "A march", "A sonata"], "A night piece", 2),
    ("Who was Chopin's famous lover?", ["George Sand", "Clara Schumann", "Cosima Wagner", "Alma Mahler"], "George Sand", 2),
    ("How many études did Chopin compose?", ["27", "20", "30", "24"], "27", 3),
    ("What is Chopin's most famous waltz?", ["Minute Waltz", "Blue Danube", "Emperor Waltz", "Voices of Spring"], "Minute Waltz", 2),

    # Vivaldi questions
    ("What year was Antonio Vivaldi born?", ["1678", "1685", "1690", "1670"], "1678", 2),
    ("In which city was Vivaldi born?", ["Venice", "Rome", "Florence", "Milan"], "Venice", 1),
    ("What is Vivaldi's most famous work?", ["The Four Seasons", "Water Music", "Messiah", "Brandenburg Concertos"], "The Four Seasons", 1),
    ("What was Vivaldi's nickname?", ["The Red Priest", "The White Swan", "The Golden Voice", "The Black Prince"], "The Red Priest", 2),
    ("What instrument did Vivaldi play?", ["Violin", "Piano", "Cello", "Flute"], "Violin", 1),
    ("How many concertos did Vivaldi compose approximately?", ["500", "300", "700", "200"], "500", 3),
    ("What was Vivaldi's other profession besides music?", ["Priest", "Doctor", "Teacher", "Lawyer"], "Priest", 2),
    ("What year did Vivaldi die?", ["1741", "1750", "1735", "1745"], "1741", 2),
    ("Which season comes first in 'The Four Seasons'?", ["Spring", "Summer", "Winter", "Autumn"], "Spring", 1),
    ("Where did Vivaldi work for most of his career?", ["Ospedale della Pietà", "St. Mark's Basilica", "Vatican", "La Scala"], "Ospedale della Pietà", 3),

    # Handel questions
    ("What year was George Frideric Handel born?", ["1685", "1678", "1690", "1700"], "1685", 2),
    ("In which country was Handel born?", ["Germany", "England", "Italy", "France"], "Germany", 1),
    ("What is Handel's most famous oratorio?", ["Messiah", "The Creation", "Elijah", "St. Matthew Passion"], "Messiah", 1),
    ("In which country did Handel spend most of his career?", ["England", "Germany", "Italy", "France"], "England", 2),
    ("What is the most famous chorus from Messiah?", ["Hallelujah", "Gloria", "Amen", "Hosanna"], "Hallelujah", 1),
    ("What year did Handel die?", ["1759", "1750", "1765", "1755"], "1759", 2),
    ("What famous water-themed work did Handel compose?", ["Water Music", "La Mer", "The Moldau", "Fountains of Rome"], "Water Music", 2),
    ("For which king did Handel compose 'Water Music'?", ["King George I", "King Louis XIV", "King Frederick II", "King Charles II"], "King George I", 3),
    ("What instrument did Handel master?", ["Organ", "Violin", "Flute", "Trumpet"], "Organ", 2),
    ("Which composer was born in the same year as Handel?", ["Johann Sebastian Bach", "Antonio Vivaldi", "Domenico Scarlatti", "Georg Telemann"], "Johann Sebastian Bach", 3),

    # Tchaikovsky questions
    ("What year was Pyotr Ilyich Tchaikovsky born?", ["1840", "1850", "1835", "1845"], "1840", 2),
    ("In which country was Tchaikovsky born?", ["Russia", "Germany", "Austria", "France"], "Russia", 1),
    ("What is Tchaikovsky's most famous ballet?", ["Swan Lake", "Giselle", "Coppélia", "La Sylphide"], "Swan Lake", 1),
    ("Which Tchaikovsky ballet features a Christmas tree?", ["The Nutcracker", "Swan Lake", "Sleeping Beauty", "Romeo and Juliet"], "The Nutcracker", 1),
    ("What year did Tchaikovsky die?", ["1893", "1900", "1890", "1895"], "1893", 2),
    ("How many symphonies did Tchaikovsky compose?", ["6", "9", "5", "8"], "6", 2),
    ("What is the nickname of Tchaikovsky's Symphony No. 6?", ["Pathétique", "Romantic", "Tragic", "Heroic"], "Pathétique", 2),
    ("What famous overture did Tchaikovsky compose about a Russian victory?", ["1812 Overture", "Russian Easter Overture", "In the Steppes of Central Asia", "Night on Bald Mountain"], "1812 Overture", 2),
    ("Which ballet was commissioned for the Imperial Mariinsky Theatre?", ["Sleeping Beauty", "Swan Lake", "The Nutcracker", "Don Quixote"], "Sleeping Beauty", 3),
    ("What is Tchaikovsky's only opera performed regularly today?", ["Eugene Onegin", "Boris Godunov", "The Queen of Spades", "Prince Igor"], "Eugene Onegin", 3),

    # Brahms questions
    ("What year was Johannes Brahms born?", ["1833", "1840", "1830", "1835"], "1833", 2),
    ("In which city was Brahms born?", ["Hamburg", "Vienna", "Leipzig", "Berlin"], "Hamburg", 2),
    ("How many symphonies did Brahms compose?", ["4", "9", "6", "3"], "4", 1),
    ("What is Brahms' most famous lullaby?", ["Brahms' Lullaby (Wiegenlied)", "Cradle Song", "Sleep Song", "Baby's Dream"], "Brahms' Lullaby (Wiegenlied)", 2),
    ("What year did Brahms die?", ["1897", "1900", "1890", "1895"], "1897", 2),
    ("Which composer was Brahms compared to constantly?", ["Beethoven", "Mozart", "Bach", "Wagner"], "Beethoven", 2),
    ("What famous work did Brahms compose for chorus and orchestra?", ["A German Requiem", "Messiah", "Mass in B minor", "Carmina Burana"], "A German Requiem", 3),
    ("In which city did Brahms spend most of his adult life?", ["Vienna", "Hamburg", "Leipzig", "Munich"], "Vienna", 2),
    ("What instrument did Brahms play as a child?", ["Piano", "Violin", "Cello", "Flute"], "Piano", 2),
    ("How many violin concertos did Brahms compose?", ["1", "2", "3", "0"], "1", 2),

    # Schubert questions
    ("What year was Franz Schubert born?", ["1797", "1800", "1795", "1805"], "1797", 2),
    ("In which city was Schubert born?", ["Vienna", "Salzburg", "Munich", "Prague"], "Vienna", 1),
    ("At what age did Schubert die?", ["31", "35", "28", "40"], "31", 2),
    ("How many symphonies did Schubert complete?", ["8", "9", "7", "10"], "8", 3),
    ("What is a 'Lied'?", ["German art song", "A dance", "A symphony", "An opera"], "German art song", 2),
    ("What is Schubert's most famous song cycle?", ["Winterreise", "Die schöne Müllerin", "Schwanengesang", "Dichterliebe"], "Winterreise", 3),
    ("What year did Schubert die?", ["1828", "1830", "1825", "1835"], "1828", 2),
    ("Which Schubert symphony is called 'Unfinished'?", ["Symphony No. 8", "Symphony No. 9", "Symphony No. 7", "Symphony No. 5"], "Symphony No. 8", 2),
    ("How many Lieder (songs) did Schubert compose approximately?", ["600", "400", "800", "300"], "600", 3),
    ("What is Schubert's most famous piano quintet?", ["Trout Quintet", "Emperor Quintet", "Rosamunde Quintet", "Death and the Maiden"], "Trout Quintet", 3),

    # Wagner questions
    ("What year was Richard Wagner born?", ["1813", "1820", "1810", "1815"], "1813", 2),
    ("In which country was Wagner born?", ["Germany", "Austria", "France", "Italy"], "Germany", 1),
    ("What is Wagner's most famous opera cycle?", ["The Ring Cycle", "The Magic Flute", "Die Meistersinger", "Parsifal"], "The Ring Cycle", 1),
    ("How many operas are in Wagner's Ring Cycle?", ["4", "3", "5", "6"], "4", 2),
    ("What year did Wagner die?", ["1883", "1890", "1880", "1885"], "1883", 2),
    ("Which Wagner opera features the famous 'Ride of the Valkyries'?", ["Die Walküre", "Das Rheingold", "Siegfried", "Götterdämmerung"], "Die Walküre", 2),
    ("What opera house did Wagner build?", ["Bayreuth Festspielhaus", "Vienna State Opera", "La Scala", "Metropolitan Opera"], "Bayreuth Festspielhaus", 3),
    ("What is Wagner's concept of total artwork called?", ["Gesamtkunstwerk", "Leitmotif", "Music Drama", "Opera seria"], "Gesamtkunstwerk", 3),
    ("Who was Wagner's second wife?", ["Cosima Wagner", "Clara Schumann", "Alma Mahler", "Mathilde Wesendonck"], "Cosima Wagner", 3),
    ("What famous march is played at weddings?", ["Bridal Chorus from Lohengrin", "Wedding March from A Midsummer Night's Dream", "Canon in D", "Ave Maria"], "Bridal Chorus from Lohengrin", 2),

    # Liszt questions
    ("What year was Franz Liszt born?", ["1811", "1815", "1820", "1810"], "1811", 2),
    ("In which country was Liszt born?", ["Hungary", "Austria", "Germany", "France"], "Hungary", 1),
    ("What instrument was Liszt famous for?", ["Piano", "Violin", "Cello", "Organ"], "Piano", 1),
    ("What is Liszt known as?", ["The greatest pianist of his time", "The father of symphony", "The king of opera", "The master of ballet"], "The greatest pianist of his time", 2),
    ("What year did Liszt die?", ["1886", "1890", "1880", "1885"], "1886", 2),
    ("How many Hungarian Rhapsodies did Liszt compose?", ["19", "15", "20", "25"], "19", 3),
    ("What innovative form did Liszt develop?", ["Symphonic poem", "Concerto", "Sonata", "Opera"], "Symphonic poem", 3),
    ("Where did Liszt spend the last years of his life?", ["Rome", "Budapest", "Paris", "Vienna"], "Rome", 2),
    ("Who was Liszt's famous daughter?", ["Cosima Wagner", "Clara Schumann", "Alma Mahler", "Fanny Mendelssohn"], "Cosima Wagner", 3),
    ("What is Liszt's most famous piano work?", ["Hungarian Rhapsody No. 2", "La Campanella", "Liebesträume", "Transcendental Études"], "Hungarian Rhapsody No. 2", 2),

    # Verdi questions
    ("What year was Giuseppe Verdi born?", ["1813", "1820", "1810", "1815"], "1813", 2),
    ("In which country was Verdi born?", ["Italy", "France", "Germany", "Austria"], "Italy", 1),
    ("What is Verdi most famous for?", ["Opera", "Symphony", "Concerto", "Chamber music"], "Opera", 1),
    ("What is Verdi's most famous opera?", ["La Traviata", "Carmen", "The Magic Flute", "Don Giovanni"], "La Traviata", 2),
    ("What year did Verdi die?", ["1901", "1900", "1895", "1905"], "1901", 2),
    ("Which Verdi opera is set in ancient Egypt?", ["Aida", "Nabucco", "Rigoletto", "Il Trovatore"], "Aida", 2),
    ("What is the famous chorus from Nabucco?", ["Va, pensiero", "La donna è mobile", "Anvil Chorus", "Triumphal March"], "Va, pensiero", 3),
    ("Which Verdi opera features a hunchbacked jester?", ["Rigoletto", "Il Trovatore", "La Traviata", "Otello"], "Rigoletto", 2),
    ("How many operas did Verdi compose?", ["28", "30", "25", "35"], "28", 3),
    ("What is Verdi's last opera?", ["Falstaff", "Otello", "Aida", "Don Carlo"], "Falstaff", 3),

    # Haydn questions
    ("What year was Joseph Haydn born?", ["1732", "1740", "1730", "1735"], "1732", 2),
    ("In which country was Haydn born?", ["Austria", "Germany", "Italy", "Hungary"], "Austria", 1),
    ("What is Haydn known as?", ["Father of the Symphony", "Father of the Opera", "Father of the Concerto", "Father of the Sonata"], "Father of the Symphony", 2),
    ("How many symphonies did Haydn compose?", ["104", "90", "120", "80"], "104", 3),
    ("What year did Haydn die?", ["1809", "1810", "1800", "1805"], "1809", 2),
    ("Which symphony is nicknamed 'Surprise'?", ["Symphony No. 94", "Symphony No. 100", "Symphony No. 101", "Symphony No. 104"], "Symphony No. 94", 2),
    ("For which aristocratic family did Haydn work for 30 years?", ["Esterházy", "Habsburg", "Bourbon", "Medici"], "Esterházy", 3),
    ("What is Haydn's most famous oratorio?", ["The Creation", "Messiah", "Elijah", "St. Matthew Passion"], "The Creation", 2),
    ("Which composer was Haydn's student?", ["Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Franz Schubert", "Franz Liszt"], "Ludwig van Beethoven", 2),
    ("What instrument did Haydn compose 83 string quartets for?", ["String quartet", "Piano trio", "Wind quintet", "String orchestra"], "String quartet", 2),

    # Mendelssohn questions
    ("What year was Felix Mendelssohn born?", ["1809", "1815", "1810", "1820"], "1809", 2),
    ("In which country was Mendelssohn born?", ["Germany", "Austria", "France", "Italy"], "Germany", 1),
    ("What is Mendelssohn's most famous work?", ["A Midsummer Night's Dream", "Swan Lake", "The Nutcracker", "The Four Seasons"], "A Midsummer Night's Dream", 2),
    ("What year did Mendelssohn die?", ["1847", "1850", "1845", "1855"], "1847", 2),
    ("At what age did Mendelssohn die?", ["38", "40", "35", "42"], "38", 2),
    ("What famous overture is from 'A Midsummer Night's Dream'?", ["Wedding March", "Bridal Chorus", "Canon in D", "Ave Maria"], "Wedding March", 2),
    ("How many symphonies did Mendelssohn compose?", ["5", "6", "4", "7"], "5", 2),
    ("Which Mendelssohn symphony is called 'Italian'?", ["Symphony No. 4", "Symphony No. 3", "Symphony No. 5", "Symphony No. 2"], "Symphony No. 4", 2),
    ("What did Mendelssohn rediscover and revive?", ["Bach's St. Matthew Passion", "Vivaldi's Four Seasons", "Handel's Messiah", "Mozart's Requiem"], "Bach's St. Matthew Passion", 3),
    ("Who was Mendelssohn's sister, also a talented composer?", ["Fanny Mendelssohn", "Clara Schumann", "Maria Anna Mozart", "Louise Farrenc"], "Fanny Mendelssohn", 3),

    # Schumann questions
    ("What year was Robert Schumann born?", ["1810", "1815", "1820", "1805"], "1810", 2),
    ("In which country was Schumann born?", ["Germany", "Austria", "France", "Poland"], "Germany", 1),
    ("Who was Schumann's wife, also a famous pianist?", ["Clara Schumann", "Fanny Mendelssohn", "Cosima Wagner", "Alma Mahler"], "Clara Schumann", 2),
    ("What year did Schumann die?", ["1856", "1860", "1850", "1855"], "1856", 2),
    ("What injury ended Schumann's piano career?", ["Hand injury", "Arm fracture", "Wrist sprain", "Shoulder dislocation"], "Hand injury", 2),
    ("How many symphonies did Schumann compose?", ["4", "5", "3", "6"], "4", 2),
    ("What is Schumann's most famous piano cycle?", ["Carnaval", "Kinderszenen", "Kreisleriana", "Papillons"], "Carnaval", 3),
    ("What famous composer was Schumann's protégé?", ["Johannes Brahms", "Franz Liszt", "Richard Wagner", "Anton Bruckner"], "Johannes Brahms", 3),
    ("What was Schumann's other profession?", ["Music critic", "Teacher", "Lawyer", "Doctor"], "Music critic", 2),
    ("Where did Schumann spend his final years?", ["Mental asylum", "His home", "Hospital", "Sanatorium"], "Mental asylum", 3),

    # Debussy questions
    ("What year was Claude Debussy born?", ["1862", "1870", "1860", "1865"], "1862", 2),
    ("In which country was Debussy born?", ["France", "Germany", "Italy", "Austria"], "France", 1),
    ("What musical style is Debussy associated with?", ["Impressionism", "Romanticism", "Baroque", "Classical"], "Impressionism", 2),
    ("What is Debussy's most famous piano piece?", ["Clair de Lune", "Moonlight Sonata", "Für Elise", "Turkish March"], "Clair de Lune", 1),
    ("What year did Debussy die?", ["1918", "1920", "1915", "1925"], "1918", 2),
    ("What is Debussy's orchestral masterpiece?", ["La Mer", "The Moldau", "Fountains of Rome", "The Pines of Rome"], "La Mer", 2),
    ("What does 'Clair de Lune' mean?", ["Moonlight", "Starlight", "Sunlight", "Twilight"], "Moonlight", 1),
    ("What is Debussy's only opera?", ["Pelléas et Mélisande", "Carmen", "La Bohème", "Madama Butterfly"], "Pelléas et Mélisande", 3),
    ("What famous ballet did Debussy compose?", ["Prélude à l'après-midi d'un faune", "The Rite of Spring", "Petrushka", "The Firebird"], "Prélude à l'après-midi d'un faune", 3),
    ("What instrument collection did Debussy write for?", ["Piano", "Violin", "Orchestra", "Chamber ensemble"], "Piano", 2),

    # Rachmaninoff questions
    ("What year was Sergei Rachmaninoff born?", ["1873", "1880", "1870", "1875"], "1873", 2),
    ("In which country was Rachmaninoff born?", ["Russia", "Germany", "France", "Austria"], "Russia", 1),
    ("What is Rachmaninoff famous for?", ["Piano concertos", "Operas", "Symphonies", "String quartets"], "Piano concertos", 2),
    ("How many piano concertos did Rachmaninoff compose?", ["4", "5", "3", "6"], "4", 2),
    ("What year did Rachmaninoff die?", ["1943", "1940", "1945", "1950"], "1943", 2),
    ("What is Rachmaninoff's most famous piano concerto?", ["Piano Concerto No. 2", "Piano Concerto No. 3", "Piano Concerto No. 1", "Piano Concerto No. 4"], "Piano Concerto No. 2", 2),
    ("Where did Rachmaninoff spend his final years?", ["United States", "Russia", "France", "Switzerland"], "United States", 2),
    ("What was Rachmaninoff known for having?", ["Very large hands", "Perfect pitch", "Photographic memory", "Exceptional sight-reading"], "Very large hands", 2),
    ("What famous choral work did Rachmaninoff compose?", ["Vespers", "Requiem", "Messiah", "Mass in B minor"], "Vespers", 3),
    ("What style is Rachmaninoff's music?", ["Late Romantic", "Impressionist", "Baroque", "Classical"], "Late Romantic", 2),

    # Dvořák questions
    ("What year was Antonín Dvořák born?", ["1841", "1850", "1840", "1845"], "1841", 2),
    ("In which country was Dvořák born?", ["Czech Republic (Bohemia)", "Austria", "Germany", "Poland"], "Czech Republic (Bohemia)", 1),
    ("What is Dvořák's most famous symphony?", ["Symphony No. 9 'From the New World'", "Symphony No. 5", "Symphony No. 7", "Symphony No. 8"], "Symphony No. 9 'From the New World'", 2),
    ("What year did Dvořák die?", ["1904", "1900", "1910", "1905"], "1904", 2),
    ("Where did Dvořák compose his 'New World Symphony'?", ["United States", "Czech Republic", "Austria", "Germany"], "United States", 2),
    ("How many symphonies did Dvořák compose?", ["9", "10", "8", "11"], "9", 2),
    ("What is Dvořák's famous chamber work?", ["American String Quartet", "Trout Quintet", "Death and the Maiden", "Emperor Quartet"], "American String Quartet", 3),
    ("What famous dance did Dvořák compose?", ["Slavonic Dances", "Hungarian Dances", "Norwegian Dances", "Spanish Dances"], "Slavonic Dances", 2),
    ("Who was Dvořák's mentor?", ["Johannes Brahms", "Franz Liszt", "Richard Wagner", "Anton Bruckner"], "Johannes Brahms", 3),
    ("What instrument did Dvořák write a famous concerto for?", ["Cello", "Violin", "Piano", "Viola"], "Cello", 2),

    # Strauss (Johann) questions
    ("What year was Johann Strauss II born?", ["1825", "1830", "1820", "1835"], "1825", 2),
    ("In which country was Strauss born?", ["Austria", "Germany", "France", "Italy"], "Austria", 1),
    ("What is Strauss known as?", ["The Waltz King", "The March King", "The Opera King", "The Symphony King"], "The Waltz King", 1),
    ("What is Strauss's most famous waltz?", ["The Blue Danube", "Emperor Waltz", "Tales from the Vienna Woods", "Voices of Spring"], "The Blue Danube", 1),
    ("What year did Strauss die?", ["1899", "1900", "1895", "1905"], "1899", 2),
    ("What is the full name of 'The Blue Danube'?", ["An der schönen blauen Donau", "Die Fledermaus", "Wiener Blut", "Frühlingsstimmen"], "An der schönen blauen Donau", 3),
    ("What is Strauss's most famous operetta?", ["Die Fledermaus", "The Merry Widow", "The Gypsy Baron", "A Night in Venice"], "Die Fledermaus", 2),
    ("Who was Johann Strauss II's father?", ["Johann Strauss I", "Franz Strauss", "Richard Strauss", "Joseph Strauss"], "Johann Strauss I", 2),
    ("In which city did Strauss primarily work?", ["Vienna", "Berlin", "Munich", "Salzburg"], "Vienna", 1),
    ("How many waltzes did Strauss compose approximately?", ["150", "100", "200", "250"], "150", 3),

    # Puccini questions
    ("What year was Giacomo Puccini born?", ["1858", "1860", "1865", "1870"], "1858", 2),
    ("In which country was Puccini born?", ["Italy", "France", "Germany", "Austria"], "Italy", 1),
    ("What is Puccini most famous for?", ["Opera", "Symphony", "Concerto", "Chamber music"], "Opera", 1),
    ("What is Puccini's most famous opera?", ["La Bohème", "Carmen", "The Magic Flute", "Don Giovanni"], "La Bohème", 2),
    ("What year did Puccini die?", ["1924", "1920", "1930", "1925"], "1924", 2),
    ("Which Puccini opera is set in Japan?", ["Madama Butterfly", "Turandot", "La Bohème", "Tosca"], "Madama Butterfly", 2),
    ("What is Puccini's last opera?", ["Turandot", "La Bohème", "Tosca", "Madama Butterfly"], "Turandot", 2),
    ("What famous aria is from Turandot?", ["Nessun Dorma", "O mio babbino caro", "Vissi d'arte", "E lucevan le stelle"], "Nessun Dorma", 2),
    ("Which opera features the aria 'O mio babbino caro'?", ["Gianni Schicchi", "La Bohème", "Tosca", "Madama Butterfly"], "Gianni Schicchi", 3),
    ("In which city is Tosca set?", ["Rome", "Paris", "Venice", "Florence"], "Rome", 2),

    # Stravinsky questions
    ("What year was Igor Stravinsky born?", ["1882", "1880", "1885", "1890"], "1882", 2),
    ("In which country was Stravinsky born?", ["Russia", "France", "Germany", "Austria"], "Russia", 1),
    ("What is Stravinsky's most famous ballet?", ["The Rite of Spring", "Swan Lake", "The Nutcracker", "Giselle"], "The Rite of Spring", 2),
    ("What year did Stravinsky die?", ["1971", "1970", "1975", "1965"], "1971", 2),
    ("What caused a riot at the premiere of 'The Rite of Spring'?", ["The controversial music and choreography", "The staging", "The costumes", "The lighting"], "The controversial music and choreography", 2),
    ("Which ballet tells the story of a Russian puppet?", ["Petrushka", "The Firebird", "The Rite of Spring", "Apollo"], "Petrushka", 2),
    ("What is Stravinsky's first major ballet?", ["The Firebird", "Petrushka", "The Rite of Spring", "Apollo"], "The Firebird", 2),
    ("Which impresario commissioned Stravinsky's early ballets?", ["Sergei Diaghilev", "George Balanchine", "Rudolf Nureyev", "Marius Petipa"], "Sergei Diaghilev", 3),
    ("Where did Stravinsky spend his final years?", ["United States", "Russia", "France", "Switzerland"], "United States", 2),
    ("What musical style did Stravinsky pioneer?", ["Neoclassicism", "Romanticism", "Impressionism", "Minimalism"], "Neoclassicism", 3),

    # Mahler questions
    ("What year was Gustav Mahler born?", ["1860", "1865", "1870", "1855"], "1860", 2),
    ("In which country was Mahler born?", ["Austria (Bohemia)", "Germany", "Czech Republic", "Hungary"], "Austria (Bohemia)", 2),
    ("What is Mahler famous for?", ["Symphonies", "Operas", "Concertos", "Chamber music"], "Symphonies", 1),
    ("How many completed symphonies did Mahler compose?", ["9", "10", "8", "11"], "9", 2),
    ("What year did Mahler die?", ["1911", "1910", "1915", "1920"], "1911", 2),
    ("What was Mahler's profession besides composing?", ["Conductor", "Pianist", "Teacher", "Music critic"], "Conductor", 2),
    ("Which Mahler symphony is nicknamed 'Symphony of a Thousand'?", ["Symphony No. 8", "Symphony No. 9", "Symphony No. 2", "Symphony No. 5"], "Symphony No. 8", 3),
    ("What is Mahler's song cycle with orchestra?", ["Das Lied von der Erde", "Kindertotenlieder", "Des Knaben Wunderhorn", "Rückert-Lieder"], "Das Lied von der Erde", 3),
    ("Where was Mahler conductor for many years?", ["Vienna Opera", "Berlin Philharmonic", "New York Philharmonic", "Leipzig Gewandhaus"], "Vienna Opera", 2),
    ("Who was Mahler's wife?", ["Alma Mahler", "Clara Schumann", "Cosima Wagner", "Fanny Mendelssohn"], "Alma Mahler", 3),

    # Rossini questions
    ("What year was Gioachino Rossini born?", ["1792", "1800", "1795", "1805"], "1792", 2),
    ("In which country was Rossini born?", ["Italy", "France", "Germany", "Austria"], "Italy", 1),
    ("What is Rossini's most famous opera?", ["The Barber of Seville", "Carmen", "La Traviata", "Don Giovanni"], "The Barber of Seville", 1),
    ("What year did Rossini die?", ["1868", "1870", "1865", "1875"], "1868", 2),
    ("What is the famous overture from 'William Tell'?", ["William Tell Overture", "The Barber of Seville Overture", "La Gazza Ladra Overture", "Semiramide Overture"], "William Tell Overture", 1),
    ("At what age did Rossini retire from opera composition?", ["37", "40", "45", "50"], "37", 3),
    ("How many operas did Rossini compose?", ["39", "30", "50", "25"], "39", 3),
    ("What type of voice is the character Figaro in 'The Barber of Seville'?", ["Baritone", "Tenor", "Bass", "Countertenor"], "Baritone", 2),
    ("What is Rossini known for in his compositions?", ["Rapid crescendos", "Slow tempos", "Dissonance", "Atonality"], "Rapid crescendos", 3),
    ("Where did Rossini spend his retirement?", ["Paris", "Rome", "Vienna", "Milan"], "Paris", 2),

    # Berlioz questions
    ("What year was Hector Berlioz born?", ["1803", "1810", "1800", "1805"], "1803", 2),
    ("In which country was Berlioz born?", ["France", "Germany", "Italy", "Austria"], "France", 1),
    ("What is Berlioz's most famous work?", ["Symphonie fantastique", "The Rite of Spring", "La Mer", "Symphony No. 9"], "Symphonie fantastique", 2),
    ("What year did Berlioz die?", ["1869", "1870", "1865", "1875"], "1869", 2),
    ("What is unique about Symphonie fantastique?", ["It tells a story of unrequited love", "It has 9 movements", "It uses no strings", "It's for piano solo"], "It tells a story of unrequited love", 2),
    ("What famous treatise did Berlioz write?", ["Treatise on Instrumentation", "Art of Fugue", "The Musical Offering", "Well-Tempered Clavier"], "Treatise on Instrumentation", 3),
    ("What is Berlioz's opera based on Virgil's Aeneid?", ["Les Troyens", "Béatrice et Bénédict", "Benvenuto Cellini", "La Damnation de Faust"], "Les Troyens", 3),
    ("What movement in Symphonie fantastique features a guillotine?", ["March to the Scaffold", "A Ball", "Scene in the Fields", "Dream of a Witches' Sabbath"], "March to the Scaffold", 3),
    ("Who was Berlioz's idol?", ["Beethoven", "Mozart", "Bach", "Haydn"], "Beethoven", 2),
    ("What is the recurring theme in Symphonie fantastique called?", ["Idée fixe", "Leitmotif", "Ground bass", "Ostinato"], "Idée fixe", 3),

    # Prokofiev questions
    ("What year was Sergei Prokofiev born?", ["1891", "1890", "1895", "1900"], "1891", 2),
    ("In which country was Prokofiev born?", ["Russia", "Germany", "France", "Austria"], "Russia", 1),
    ("What is Prokofiev's most famous ballet?", ["Romeo and Juliet", "Swan Lake", "The Nutcracker", "Sleeping Beauty"], "Romeo and Juliet", 2),
    ("What year did Prokofiev die?", ["1953", "1950", "1955", "1960"], "1953", 2),
    ("What famous children's work did Prokofiev compose?", ["Peter and the Wolf", "The Nutcracker", "The Firebird", "Petrushka"], "Peter and the Wolf", 1),
    ("How many symphonies did Prokofiev compose?", ["7", "9", "6", "8"], "7", 2),
    ("What is unique about 'Peter and the Wolf'?", ["Each character is represented by an instrument", "It has no melody", "It's for solo piano", "It's in Latin"], "Each character is represented by an instrument", 2),
    ("Which Prokofiev ballet is based on Shakespeare?", ["Romeo and Juliet", "Cinderella", "The Stone Flower", "The Tale of the Stone Flower"], "Romeo and Juliet", 2),
    ("What is Prokofiev's famous piano concerto?", ["Piano Concerto No. 3", "Piano Concerto No. 2", "Piano Concerto No. 1", "Piano Concerto No. 5"], "Piano Concerto No. 3", 3),
    ("What style is Prokofiev's music known for?", ["Neoclassicism and modernism", "Romanticism", "Baroque", "Impressionism"], "Neoclassicism and modernism", 3),

    # Shostakovich questions
    ("What year was Dmitri Shostakovich born?", ["1906", "1910", "1905", "1900"], "1906", 2),
    ("In which country was Shostakovich born?", ["Russia", "Germany", "Poland", "Ukraine"], "Russia", 1),
    ("How many symphonies did Shostakovich compose?", ["15", "13", "17", "12"], "15", 2),
    ("What year did Shostakovich die?", ["1975", "1970", "1980", "1965"], "1975", 2),
    ("Which Shostakovich symphony is called 'Leningrad'?", ["Symphony No. 7", "Symphony No. 5", "Symphony No. 10", "Symphony No. 11"], "Symphony No. 7", 2),
    ("What political regime did Shostakovich live under?", ["Soviet Union", "Nazi Germany", "Fascist Italy", "Imperial Russia"], "Soviet Union", 1),
    ("What is Shostakovich's most famous string quartet?", ["String Quartet No. 8", "String Quartet No. 1", "String Quartet No. 15", "String Quartet No. 5"], "String Quartet No. 8", 3),
    ("How many string quartets did Shostakovich compose?", ["15", "12", "17", "20"], "15", 3),
    ("What was Shostakovich's relationship with Stalin?", ["Difficult and dangerous", "Close friendship", "Indifferent", "Collaborative"], "Difficult and dangerous", 2),
    ("What is a recurring theme in Shostakovich's music?", ["Political oppression", "Love and romance", "Nature", "Religion"], "Political oppression", 2),

    # Saint-Saëns questions
    ("What year was Camille Saint-Saëns born?", ["1835", "1840", "1830", "1845"], "1835", 2),
    ("In which country was Saint-Saëns born?", ["France", "Germany", "Italy", "Austria"], "France", 1),
    ("What is Saint-Saëns' most famous work?", ["The Carnival of the Animals", "The Four Seasons", "Pictures at an Exhibition", "Night on Bald Mountain"], "The Carnival of the Animals", 1),
    ("What year did Saint-Saëns die?", ["1921", "1920", "1925", "1915"], "1921", 2),
    ("What famous movement features a swan?", ["The Swan", "The Elephant", "The Aquarium", "The Aviary"], "The Swan", 1),
    ("How many symphonies did Saint-Saëns compose?", ["5", "6", "4", "7"], "5", 2),
    ("What is Saint-Saëns' most famous symphony?", ["Symphony No. 3 'Organ Symphony'", "Symphony No. 2", "Symphony No. 1", "Symphony No. 4"], "Symphony No. 3 'Organ Symphony'", 2),
    ("What opera did Saint-Saëns compose about a biblical figure?", ["Samson and Delilah", "Moses", "David and Goliath", "Solomon"], "Samson and Delilah", 2),
    ("What instrument is featured in Symphony No. 3?", ["Organ", "Piano", "Harp", "Saxophone"], "Organ", 2),
    ("What was Saint-Saëns besides a composer?", ["Pianist and organist", "Violinist", "Conductor", "Music critic"], "Pianist and organist", 2),

    # Bizet questions
    ("What year was Georges Bizet born?", ["1838", "1840", "1835", "1845"], "1838", 2),
    ("In which country was Bizet born?", ["France", "Germany", "Italy", "Spain"], "France", 1),
    ("What is Bizet's most famous opera?", ["Carmen", "La Traviata", "Madama Butterfly", "The Magic Flute"], "Carmen", 1),
    ("What year did Bizet die?", ["1875", "1880", "1870", "1885"], "1875", 2),
    ("At what age did Bizet die?", ["36", "40", "30", "45"], "36", 2),
    ("Where is Carmen set?", ["Seville, Spain", "Paris, France", "Rome, Italy", "Vienna, Austria"], "Seville, Spain", 2),
    ("What is the famous aria from Carmen?", ["Habanera", "Nessun Dorma", "O mio babbino caro", "Caro nome"], "Habanera", 2),
    ("What is the occupation of Carmen?", ["Factory worker", "Singer", "Dancer", "Seamstress"], "Factory worker", 2),
    ("What dance rhythm is in the Habanera?", ["Cuban", "Spanish", "French", "Italian"], "Cuban", 3),
    ("What is Bizet's orchestral suite?", ["L'Arlésienne", "Pictures at an Exhibition", "The Carnival of the Animals", "Mother Goose Suite"], "L'Arlésienne", 3),

    # Grieg questions
    ("What year was Edvard Grieg born?", ["1843", "1840", "1845", "1850"], "1843", 2),
    ("In which country was Grieg born?", ["Norway", "Sweden", "Denmark", "Finland"], "Norway", 1),
    ("What is Grieg's most famous work?", ["Peer Gynt", "The Four Seasons", "The Moldau", "Finlandia"], "Peer Gynt", 2),
    ("What year did Grieg die?", ["1907", "1910", "1905", "1900"], "1907", 2),
    ("What is the famous piece from Peer Gynt?", ["In the Hall of the Mountain King", "Morning Mood", "Anitra's Dance", "Solveig's Song"], "In the Hall of the Mountain King", 1),
    ("How many piano concertos did Grieg compose?", ["1", "2", "3", "0"], "1", 2),
    ("In which key is Grieg's Piano Concerto?", ["A minor", "C major", "E minor", "D major"], "A minor", 3),
    ("What type of music did Grieg often incorporate?", ["Norwegian folk music", "Spanish flamenco", "Irish jigs", "Scottish reels"], "Norwegian folk music", 2),
    ("What famous playwright wrote Peer Gynt?", ["Henrik Ibsen", "August Strindberg", "Anton Chekhov", "George Bernard Shaw"], "Henrik Ibsen", 3),
    ("What is Grieg's collection of piano pieces called?", ["Lyric Pieces", "Songs Without Words", "Moments Musicaux", "Impromptus"], "Lyric Pieces", 3),

    # Ravel questions
    ("What year was Maurice Ravel born?", ["1875", "1880", "1870", "1885"], "1875", 2),
    ("In which country was Ravel born?", ["France", "Germany", "Italy", "Austria"], "France", 1),
    ("What is Ravel's most famous orchestral work?", ["Boléro", "La Mer", "The Rite of Spring", "Pictures at an Exhibition"], "Boléro", 1),
    ("What year did Ravel die?", ["1937", "1940", "1935", "1930"], "1937", 2),
    ("What makes Boléro unique?", ["It repeats the same melody continuously", "It has no melody", "It's atonal", "It uses only percussion"], "It repeats the same melody continuously", 2),
    ("What musical style is Ravel associated with?", ["Impressionism", "Romanticism", "Baroque", "Classical"], "Impressionism", 2),
    ("What is Ravel's famous piano work?", ["Gaspard de la nuit", "Clair de Lune", "Moonlight Sonata", "Turkish March"], "Gaspard de la nuit", 3),
    ("What ballet did Ravel compose?", ["Daphnis et Chloé", "The Rite of Spring", "Petrushka", "The Firebird"], "Daphnis et Chloé", 3),
    ("What orchestration did Ravel create?", ["Pictures at an Exhibition by Mussorgsky", "Night on Bald Mountain by Mussorgsky", "Carnival of the Animals by Saint-Saëns", "Peer Gynt by Grieg"], "Pictures at an Exhibition by Mussorgsky", 3),
    ("What is Ravel's piano concerto for left hand written for?", ["A one-armed pianist", "Children", "Beginners", "Competition"], "A one-armed pianist", 3),

    # Paganini questions
    ("What year was Niccolò Paganini born?", ["1782", "1780", "1785", "1790"], "1782", 2),
    ("In which country was Paganini born?", ["Italy", "France", "Germany", "Austria"], "Italy", 1),
    ("What instrument was Paganini famous for?", ["Violin", "Piano", "Cello", "Flute"], "Violin", 1),
    ("What year did Paganini die?", ["1840", "1845", "1835", "1850"], "1840", 2),
    ("How many violin caprices did Paganini compose?", ["24", "20", "30", "18"], "24", 2),
    ("What was Paganini known as?", ["The Devil's Violinist", "The Violin King", "The Master Virtuoso", "The Italian Maestro"], "The Devil's Violinist", 2),
    ("What is Paganini's most famous caprice?", ["Caprice No. 24", "Caprice No. 1", "Caprice No. 13", "Caprice No. 20"], "Caprice No. 24", 2),
    ("Why was Paganini called 'The Devil's Violinist'?", ["His extraordinary technical abilities", "His appearance", "His behavior", "His compositions"], "His extraordinary technical abilities", 2),
    ("How many violin concertos did Paganini compose?", ["6", "5", "4", "7"], "6", 3),
    ("What technique did Paganini popularize?", ["Left-hand pizzicato", "Double stopping", "Vibrato", "Glissando"], "Left-hand pizzicato", 3),

    # Bruckner questions
    ("What year was Anton Bruckner born?", ["1824", "1830", "1820", "1835"], "1824", 2),
    ("In which country was Bruckner born?", ["Austria", "Germany", "Czech Republic", "Hungary"], "Austria", 1),
    ("What is Bruckner famous for?", ["Symphonies", "Operas", "Concertos", "Chamber music"], "Symphonies", 1),
    ("How many symphonies did Bruckner compose?", ["11", "9", "12", "10"], "11", 3),
    ("What year did Bruckner die?", ["1896", "1900", "1890", "1895"], "1896", 2),
    ("What was Bruckner's other profession?", ["Church organist", "Teacher", "Conductor", "Music critic"], "Church organist", 2),
    ("What is distinctive about Bruckner's symphonies?", ["They are very long", "They are very short", "They use no strings", "They are for solo piano"], "They are very long", 2),
    ("Which composer did Bruckner admire greatly?", ["Richard Wagner", "Johannes Brahms", "Franz Liszt", "Giuseppe Verdi"], "Richard Wagner", 2),
    ("What is Bruckner's most performed symphony?", ["Symphony No. 4 'Romantic'", "Symphony No. 7", "Symphony No. 9", "Symphony No. 5"], "Symphony No. 4 'Romantic'", 3),
    ("What did Bruckner constantly do to his symphonies?", ["Revised them", "Performed them", "Published them", "Destroyed them"], "Revised them", 2),

    # Sibelius questions
    ("What year was Jean Sibelius born?", ["1865", "1870", "1860", "1875"], "1865", 2),
    ("In which country was Sibelius born?", ["Finland", "Sweden", "Norway", "Denmark"], "Finland", 1),
    ("What is Sibelius' most famous work?", ["Finlandia", "The Moldau", "Peer Gynt", "Night on Bald Mountain"], "Finlandia", 1),
    ("What year did Sibelius die?", ["1957", "1950", "1960", "1945"], "1957", 2),
    ("How many symphonies did Sibelius compose?", ["7", "9", "6", "8"], "7", 2),
    ("What is Sibelius' famous violin concerto?", ["Violin Concerto in D minor", "Violin Concerto in E minor", "Violin Concerto in A major", "Violin Concerto in C major"], "Violin Concerto in D minor", 2),
    ("What does 'Finlandia' represent?", ["Finnish nationalism", "Finnish landscape", "Finnish mythology", "Finnish history"], "Finnish nationalism", 2),
    ("What is Sibelius' tone poem about a swan?", ["The Swan of Tuonela", "Swan Lake", "The Dying Swan", "The Wild Swan"], "The Swan of Tuonela", 3),
    ("How long did Sibelius live?", ["91 years", "80 years", "85 years", "95 years"], "91 years", 3),
    ("What did Sibelius stop composing for the last 30 years of his life?", ["Major works", "Small pieces", "Songs", "Chamber music"], "Major works", 3),

    # Elgar questions
    ("What year was Edward Elgar born?", ["1857", "1860", "1855", "1865"], "1857", 2),
    ("In which country was Elgar born?", ["England", "Scotland", "Wales", "Ireland"], "England", 1),
    ("What is Elgar's most famous work?", ["Enigma Variations", "The Planets", "Pomp and Circumstance", "Land of Hope and Glory"], "Enigma Variations", 2),
    ("What year did Elgar die?", ["1934", "1930", "1940", "1935"], "1934", 2),
    ("What is the most famous of Elgar's Pomp and Circumstance Marches?", ["March No. 1", "March No. 2", "March No. 3", "March No. 4"], "March No. 1", 2),
    ("What is 'Land of Hope and Glory' based on?", ["Pomp and Circumstance March No. 1", "Enigma Variations", "Cello Concerto", "Symphony No. 1"], "Pomp and Circumstance March No. 1", 3),
    ("What is Elgar's famous concerto?", ["Cello Concerto in E minor", "Violin Concerto in B minor", "Piano Concerto in A minor", "Viola Concerto in D major"], "Cello Concerto in E minor", 2),
    ("How many symphonies did Elgar complete?", ["2", "3", "1", "4"], "2", 2),
    ("What is special about the Enigma Variations?", ["Each variation portrays a friend", "It has no theme", "It's for solo piano", "It's in Latin"], "Each variation portrays a friend", 3),
    ("What was Elgar's wife's profession?", ["Author and poet", "Singer", "Pianist", "Violinist"], "Author and poet", 3),
]

# Add questions to quiz
question_id = 1
for q_text, options, answer, difficulty in questions_data:
    question = {
        "id": question_id,
        "uuid": str(uuid.uuid4()),
        "question": q_text,
        "difficulty_level": difficulty,
        "options": options,
        "answer": answer
    }
    quiz["questions"].append(question)
    question_id += 1

# Print quiz as JSON
print(json.dumps(quiz, ensure_ascii=False, indent=2))
print(f"\nTotal questions generated: {len(quiz['questions'])}", file=sys.stderr)

