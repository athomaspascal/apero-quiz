
-- Script to link existing users to their countries
-- Execute this script if users were created before the country linking feature

-- Link admin to France
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'FRA')
WHERE email = 'administrateur@quiz.admin';

-- Link famous people to their countries

-- USA (26 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'USA')
WHERE email IN (
    'barack.obama@public.quiz',
    'martin.luther.king.jr@public.quiz',
    'abraham.lincoln@public.quiz',
    'steve.jobs@public.quiz',
    'bill.gates@public.quiz',
    'mark.zuckerberg@public.quiz',
    'oprah.winfrey@public.quiz',
    'walt.disney@public.quiz',
    'michael.jackson@public.quiz',
    'elvis.presley@public.quiz',
    'madonna@public.quiz',
    'beyonc@public.quiz',
    'muhammad.ali@public.quiz',
    'serena.williams@public.quiz',
    'michael.jordan@public.quiz',
    'tiger.woods@public.quiz',
    'neil.armstrong@public.quiz',
    'carl.sagan@public.quiz',
    'rosa.parks@public.quiz',
    'helen.keller@public.quiz',
    'george.washington@public.quiz',
    'thomas.jefferson@public.quiz',
    'franklin.d.roosevelt@public.quiz',
    'john.f.kennedy@public.quiz',
    'mark.twain@public.quiz',
    'ernest.hemingway@public.quiz',
    'toni.morrison@public.quiz',
    'maya.angelou@public.quiz'
);

-- United Kingdom (15 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'GBR')
WHERE email IN (
    'winston.churchill@public.quiz',
    'charles.darwin@public.quiz',
    'isaac.newton@public.quiz',
    'william.shakespeare@public.quiz',
    'the.beatles@public.quiz',
    'stephen.hawking@public.quiz',
    'jane.goodall@public.quiz',
    'florence.nightingale@public.quiz',
    'elizabeth.ii@public.quiz',
    'margaret.thatcher@public.quiz',
    'virginia.woolf@public.quiz',
    'jane.austen@public.quiz',
    'j.k..rowling@public.quiz',
    'george.orwell@public.quiz',
    'agatha.christie@public.quiz'
);

-- France (8 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'FRA')
WHERE email IN (
    'coco.chanel@public.quiz',
    'napoleon.bonaparte@public.quiz',
    'joan.of.arc@public.quiz',
    'charles.de.gaulle@public.quiz',
    'simone.de.beauvoir@public.quiz',
    'victor.hugo@public.quiz',
    'voltaire@public.quiz',
    'molire@public.quiz'
);

-- Germany (6 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'DEU')
WHERE email IN (
    'albert.einstein@public.quiz',
    'ludwig.van.beethoven@public.quiz',
    'anne.frank@public.quiz',
    'karl.marx@public.quiz',
    'friedrich.nietzsche@public.quiz',
    'angela.merkel@public.quiz'
);

-- Greece (4 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'GRC')
WHERE email IN (
    'socrates@public.quiz',
    'plato@public.quiz',
    'aristotle@public.quiz',
    'alexander.the.great@public.quiz'
);

-- Argentina (4 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'ARG')
WHERE email IN (
    'lionel.messi@public.quiz',
    'pope.francis@public.quiz',
    'eva.pern@public.quiz',
    'che.guevara@public.quiz'
);

-- Italy (3 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'ITA')
WHERE email IN (
    'leonardo.da.vinci@public.quiz',
    'julius.caesar@public.quiz',
    'dante.alighieri@public.quiz'
);

-- Austria (2 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'AUT')
WHERE email IN (
    'wolfgang.mozart@public.quiz',
    'sigmund.freud@public.quiz'
);

-- Spain (2 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'ESP')
WHERE email IN (
    'pablo.picasso@public.quiz',
    'miguel.de.cervantes@public.quiz'
);

-- South Africa (2 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'ZAF')
WHERE email IN (
    'nelson.mandela@public.quiz',
    'elon.musk@public.quiz'
);

-- China (2 users)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'CHN')
WHERE email IN (
    'confucius@public.quiz',
    'mao.zedong@public.quiz'
);

-- Netherlands (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'NLD')
WHERE email = 'vincent.van.gogh@public.quiz';

-- Mexico (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'MEX')
WHERE email = 'frida.kahlo@public.quiz';

-- Poland (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'POL')
WHERE email = 'marie.curie@public.quiz';

-- Switzerland (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'CHE')
WHERE email = 'roger.federer@public.quiz';

-- Portugal (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'PRT')
WHERE email = 'cristiano.ronaldo@public.quiz';

-- Brasil (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'BRA')
WHERE email = 'pel@public.quiz';

-- Colombia (1 user)
UPDATE users SET country_id = (SELECT country_id FROM countries WHERE sigle = 'COL')
WHERE email = 'gabriel.garca.mrquez@public.quiz';

-- Note: The following users cannot be linked because their countries are not in the system yet:
-- India (IND): Mother Teresa, Mahatma Gandhi, Buddha, Dalai Lama, Indira Gandhi
-- Russia (RUS): Yuri Gagarin, Vladimir Lenin, Joseph Stalin, Leo Tolstoy, Fyodor Dostoevsky
-- Egypt (EGY): Cleopatra
-- Jamaica (JAM): Usain Bolt
-- Pakistan (PAK): Malala Yousafzai
-- Israel (ISR): Jesus Christ
-- Saudi Arabia (SAU): Prophet Muhammad
-- Mongolia (MNG): Genghis Khan

-- To add these countries and link users, first add the countries to the countries table,
-- then run similar UPDATE statements.

