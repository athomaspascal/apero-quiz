# Guide de configuration OAuth2

Ce guide explique comment configurer l'authentification OAuth2 avec Google, Facebook et LinkedIn pour votre application Quiz.

## Prérequis

L'application est maintenant configurée avec Spring Security OAuth2 Client. Vous devez obtenir les identifiants OAuth2 de chaque fournisseur.

## Configuration Google OAuth2

1. Accédez à la [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API Google+ (Google+ API)
4. Allez dans "Identifiants" > "Créer des identifiants" > "ID client OAuth 2.0"
5. Configurez l'écran de consentement OAuth si nécessaire
6. Pour le type d'application, sélectionnez "Application Web"
7. Ajoutez les URI de redirection autorisées :
   - `http://localhost:8080/login/oauth2/code/google`
   - Pour production : `https://votre-domaine.com/login/oauth2/code/google`
8. Copiez le "Client ID" et le "Client Secret"
9. Dans `application.properties`, remplacez :
   - `YOUR_GOOGLE_CLIENT_ID` par votre Client ID
   - `YOUR_GOOGLE_CLIENT_SECRET` par votre Client Secret

## Configuration Facebook OAuth2

1. Accédez à [Facebook Developers](https://developers.facebook.com/)
2. Créez une nouvelle application ou sélectionnez une application existante
3. Dans le tableau de bord, ajoutez le produit "Facebook Login"
4. Configurez les paramètres OAuth :
   - URI de redirection OAuth valides : `http://localhost:8080/login/oauth2/code/facebook`
   - Pour production : `https://votre-domaine.com/login/oauth2/code/facebook`
5. Dans "Paramètres" > "Général", copiez l'ID de l'application et la clé secrète
6. Dans `application.properties`, remplacez :
   - `YOUR_FACEBOOK_CLIENT_ID` par votre App ID
   - `YOUR_FACEBOOK_CLIENT_SECRET` par votre App Secret

## Configuration LinkedIn OAuth2

1. Accédez à [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Créez une nouvelle application
3. Dans l'onglet "Auth", ajoutez les URL de redirection autorisées :
   - `http://localhost:8080/login/oauth2/code/linkedin`
   - Pour production : `https://votre-domaine.com/login/oauth2/code/linkedin`
4. Demandez l'accès aux produits suivants :
   - "Sign In with LinkedIn using OpenID Connect"
5. Copiez le "Client ID" et le "Client Secret"
6. Dans `application.properties`, remplacez :
   - `YOUR_LINKEDIN_CLIENT_ID` par votre Client ID
   - `YOUR_LINKEDIN_CLIENT_SECRET` par votre Client Secret

## Test de l'authentification

1. Après avoir configuré les identifiants, redémarrez l'application
2. Accédez à la page de connexion (`http://localhost:8080/login`)
3. Vous verrez maintenant trois boutons supplémentaires :
   - "Google" (bleu)
   - "Facebook" (bleu foncé)
   - "LinkedIn" (bleu LinkedIn)
4. Cliquez sur l'un des boutons pour tester la connexion

## Modifications de la base de données

L'entité `User` a été mise à jour avec deux nouveaux champs :
- `oauthProvider` : le nom du fournisseur OAuth2 (google, facebook, linkedin)
- `oauthProviderId` : l'identifiant unique de l'utilisateur chez le fournisseur

Ces champs permettent de :
- Lier un compte OAuth2 à un utilisateur existant (par email)
- Créer automatiquement un compte pour les nouveaux utilisateurs OAuth2
- Permettre à un utilisateur d'avoir plusieurs méthodes de connexion

## Sécurité

- Les mots de passe des utilisateurs OAuth2 sont vides (ils ne sont pas nécessaires)
- Les utilisateurs peuvent se connecter soit avec leur email/mot de passe, soit via OAuth2
- Si un utilisateur s'inscrit avec un email, puis se connecte via OAuth2 avec le même email, les comptes sont automatiquement liés

## URLs importantes

- Page de connexion : `/login`
- Redirection OAuth2 : `/oauth2/authorization/{provider}` (géré automatiquement)
- Callback OAuth2 : `/login/oauth2/code/{provider}` (géré automatiquement)
- Succès de connexion : `/` (page d'accueil)

## Dépannage

Si vous rencontrez des problèmes :

1. Vérifiez que les URI de redirection sont correctement configurés chez chaque fournisseur
2. Assurez-vous que les identifiants sont correctement copiés dans `application.properties`
3. Vérifiez les logs de l'application pour plus de détails sur les erreurs
4. Assurez-vous que votre application est accessible via l'URL configurée (localhost:8080 ou votre domaine)

## Mode développement vs Production

### Développement (localhost)
- Utilisez `http://localhost:8080` comme URL de base
- Les fournisseurs OAuth2 doivent avoir cette URL dans leurs redirections autorisées

### Production
- Utilisez votre domaine HTTPS : `https://votre-domaine.com`
- Mettez à jour toutes les URI de redirection chez les fournisseurs
- Assurez-vous d'utiliser HTTPS (requis par la plupart des fournisseurs)

