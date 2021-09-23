��    /      �  C           �     g  �  h  P     �
  8   �
  $     R   1     �     �     �     �  N   �     E     X     m     }     �     �     �     �     �     �     �  &   �      #  �   D     �     �     �       
   !  /   ,  8   \     �  %   �  '   �  8   �     3  (   @  &   i     �     �     �  .   �     �     �  -    �   5  �    5       I  H   i  6   �  o   �  $   Y     ~  "   �     �  e   �     ?     [     s     �     �     �     �     �     �     �       (   %  *   N  �   y          $  &   >  )   e     �  >   �  H   �  !   '  1   I  5   {  <   �     �  9     &   @     g     �     �  =   �     �     �                  #                         $   
                        +      -                                    *   )       	                 ,             (       !   "   '   .          &             %               /                                   Full path: {authenticator_path}
                ID: {authenticator_uid}
                User: {authenticator_user}
                Password hint: {authenticator_passphrase_hint}
                     On this page, you can initialize an authenticator inside an empty folder; this authenticator actually consists in metadata files as well as a set of asymmetric keypairs.
        
        To proceed, you have to input your user name or pseudo, a long passphrase (e.g. consisting of 4 different words), and a public hint to help your remember your passphrase later.
        
        You should keep your passphrase somewhere safe (in a digital password manager, on a paper in a vault...), because if you forget any of its aspects (upper/lower case, accents, spaces...), there is no way to recover it.
                 On this page, you can manage your authenticators, which are actually digital keychains identified by unique IDs.
        
        These keychains contain both public keys, which can be freely shared, and their corresponding private keys, protected by passphrases, which must be kept hidden.
        
        Authenticators can be stored in your user profile or in a custom folder, especially at the root of removable devices.
        
        You can initialize new authenticators from scratch, import/export them from/to ZIP archives, or check their integrity by providing their passphrases.
        
        Note that if you destroy an authenticator and all its exported ZIP archives, the WitnessAngel recordings which used it as a trusted third party might not be decryptable anymore (unless they used a shared secret with other trusted third parties).
         Abnormal error caught: %s All authentication data from folder %s has been removed. Authenticator archive exported to %s Authenticator archive unpacked from %s, its integrity has not been checked though. Authenticator creation page Authenticator initialized Authenticator management page Authenticator not initialized Beware, this might make encrypted data using these keys impossible to decrypt. Checkup result: %s Create Authenticator Custom location Deletion is over Destroy authenticator Drive: {drive} ({label}) Export successful Failure Find Full path: %s Import successful Initialization successfully completed. Keypairs successfully tested: %s Keypairs tested: {keypair_count}
Missing private keys: {missing_private_keys}
Wrong passphrase for keys:  {undecodable_private_keys} Language Manage Authenticators No valid location selected Operation failed, check logs. Passphrase Passphrase must be at least %s characters long. Please enter a username, passphrase and passphrase hint. Please select a folder Please select an authenticator folder Please select an authenticator location Please wait a few seconds, initialization is in process. Sanity check Selected folder is invalid
Full path: %s Size: {size}, Filesystem: {filesystem} Stored inside system disk Success Target: Test integrity and passphrase of authenticator User Profile Validation error Project-Id-Version: WitnessAngelGuilib
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2021-09-23 23:21+0200
Last-Translator: Pascal <pythoniks@gmail.com>
Language-Team: Nothing
Language: fr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Virtaal 0.7.1
                 Chemin complet : {authenticator_path}
                ID : {authenticator_uid}
                Utilisateur : {authenticator_user}
                Indice de phrase secrète : {authenticator_passphrase_hint}         Sur cette page, vous pouvez initialiser un authentifieur dans un dossier vide ; cet authentifieur consiste en réalité en des fichiers de métadonnées, ainsi qu'en un ensemble de paires de clés asymétriques.
        
        Pour continuer, vous devez entrer votre nom d'utilisateur ou pseudo, une longue phrase secrète (par exemple, composée de 4 mots différents), et un indice public pour vous aider à vous souvenir de votre phrase secrète plus tard.
        
        Vous devez conserver votre phrase secrète en lieu sûr (dans un gestionnaire de mots de passe numérique, sur un papier dans un coffre-fort...), car si vous oubliez l'un de ses aspects (majuscules/minuscules, accents, espaces...), il n'y a aucun moyen de la récupérer.
                 Sur cette page, vous pouvez gérer vos authentifieurs, qui sont en fait des trousseaux de clés numériques identifiés par des ID uniques.
        
        Ces trousseaux contiennent à la fois des clés publiques, qui peuvent être partagées librement, et les clés privées correspondantes, protégées par des phrases secrètes, qui doivent rester cachées.
        
        Les authentifieurs peuvent être stockés dans votre profil utilisateur ou dans un dossier personnalisé, notamment à la racine des périphériques amovibles.
        
        Vous pouvez initialiser de nouveaux authentifieurs à partir de zéro, les importer/exporter depuis/vers des archives ZIP, ou vérifier leur intégrité en fournissant leurs phrases secrètes.
        
        Notez que si vous détruisez un authentifieurs et toutes ses archives ZIP exportées, les enregistrements WitnessAngel qui l'utilisaient en tant que tiers de confiance risquent de ne plus pouvoir être déchiffrés (à moins qu'ils n'aient utilisé un secret partagé avec d'autres tiers de confiance). Erreur anormale détectée : %s Toutes les données d'authentifieur du dossier %s ont été supprimées. L'archive de l'authentifieur a été exportée vers %s L'archive d'authentifieur a été décompressée depuis %s, son intégrité n'a cependant pas été vérifiée. Page de création de l'authentifieur Authentifieur initialisé Page de gestion de l'authentifieur Authentifieur non initialisé Attention, cela peut rendre impossible le déchiffrement des données chiffrées utilisant ces clés. Résultat du contrôle : %s Créer un Authentifieur Emplacement personnalisé Destruction terminée Détruire l'authentifieur Disque : {drive} ({label}) Exportation réussie Échec Trouver Chemin complet : %s Importation réussie Initialisation complétée avec succès. Paires de clés testées avec succès : %s Paires de clés testées : {keypair_count}
Clés privées manquantes : {missing_private_keys}
Mauvaise phrase secrète pour les clés :  {undecodable_private_keys} Langue Gérer les Authentifieurs Aucun emplacement valide sélectionné Opération échouée, vérifiez les logs. Phrase secrète La phrase secrète doit faire au moins %s caractères de long. Veuillez entrer un nom d'utilisateur, une phrase secrète et son indice. Veuillez sélectionner un dossier Veuillez sélectionner un dossier d'authentifieur Veuillez sélectionner un emplacement d'authentifieur Veuillez attendre quelques secondes, initialisation en cours Contrôle d'intégrité Le dossier sélectionné est invalide
Chemin complet : %s Taille : {size}, Format : {filesystem} Stocké dans le disque système Succès Cible : Tester l'intégrité et la phrase secrète de l'authentifieur Profil Utilisateur Erreur de validation 