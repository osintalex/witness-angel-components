��    �      �  �   �	      �  �   �  �   �  �   �  g  �  h  �  u  ^     �     �       8        Q  N   p  3   �     �  $     R   )     |     �  ,   �     �     �          8     Q     `     e  $   r  N   �     �     �                    0  &   6     ]  !   e     �     �     �  #   �  
     7        E     V     k     {     �     �     �     �     �  F   �       B   ,  "   o  8   �  &   �  *   �  3        Q     X     m          �     �     �     �     �     �     �     �       &   !  
   H      S  -   t     �     �     �  !   �     �  T         j  �   �              &   /      V   	   d      n      v   )   y      �      �   '   �      �   +   !     ;!     V!     u!  	   �!  
   �!  1   �!     �!  /   �!     "     :"  8   C"     |"  %   �"  '   �"  #   �"  "   #  %   (#  9   N#  5   �#  A   �#      $     $     $  !   &$  !   H$  ,   j$     �$     �$  #   �$     �$     �$  &   �$  E   %     [%     k%     z%     �%  "   �%  .   �%  6   �%  @   %&  '   f&     �&  	   �&  (   �&     �&  $   �&      '  $   %'     J'     N'  �   V'  i   �'     V(  W  t(  �   �)  �   �*  �   �+  �  �,  4  �/  �  �3  !   g5     �5     �5  H   �5  #   6  J   26  :   }6     �6  6   �6  o   7  !   t7     �7  -   �7     �7  "   �7     8     :8     Y8     i8     p8  &   w8  e   �8      9     %9  	   -9     79     T9     p9  8   w9  	   �9  +   �9  $   �9  (   :  %   4:  *   Z:  
   �:  <   �:     �:     �:     �:     ;     #;  	   ?;     I;  	   _;     i;  Q   �;     �;  E   �;      6<  I   W<  1   �<  <   �<  E   =     V=     _=     x=     �=     �=  &   �=     �=     �=     �=     �=  (   �=  (   >     G>  (   \>     �>  *   �>  3   �>     �>     ?     ?  /   6?  $   f?  W   �?  *   �?  �   @     �@     �@  -   �@     A     A     A     (A  /   ,A     \A     tA  8   �A     �A  ;   �A  &   %B     LB  )   kB     �B     �B  B   �B     �B  >   
C  %   IC     oC  H   {C  !   �C  1   �C  5   D  4   ND  2   �D  8   �D  Z   �D  B   JE  P   �E     �E     �E     �E  (   
F  $   3F  7   XF  !   �F     �F  1   �F  
   �F     G  &   G  f   :G     �G     �G     �G     �G  (   �G  =    H  4   ^H  ;   �H  $   �H     �H     I  /   I     CI  '   XI  (   �I  .   �I     �I     �I  �   �I  y   �J     K                    |   b   s   <   G           �   {           A       Y   l   �   ,   R       3   M   N   �   r           �   5   8   0               P   K                      h      g   '              H   t   1           F   m   C   (      j   d          �   u   q       B      :   �   o       2   L           !           X          #       )             ]       ^       S       _      e   �           [   }   �   �   	   .   �   =   �   J           Z       y      �   i   $   T       +   �      f                     "      
   �       �       V   W      -   v   k       ?         �   ~       &       U       @       x   %   I   �       z   c   �   �   �   ;          O   /   9              �       p   �   n       7   Q   �   `   �   w   �      6      �   *       E   D               >             \   a   4                            Gateway: {gateway}
                        Remote status: {status}
                        Message: {message}
                        
                        Authenticator ID: {keystore_uid}
                                           Error details:
                           Exceeding key(s) in remote: {exceeding_keys_in_remote}
                           Missing key(s) in remote: {missing_keys_in_remote}
                                       Path: {authenticator_dir}
                    ID: {keystore_uid}
                    User: {keystore_owner}
                    Password hint: {keystore_passphrase_hint}
                         On this page, you can initialize an authenticator inside an empty folder; this authenticator actually consists in metadata files as well as a set of asymmetric keypairs.
        
        To proceed, you have to input your user name or pseudo, a long passphrase (e.g. consisting of 4 different words), and a public hint to help your remember your passphrase later.
        
        You should keep your passphrase somewhere safe (in a digital password manager, on a paper in a vault...), because if you forget any of its aspects (upper/lower case, accents, spaces...), there is no way to recover it.
                 On this page, you can manage your authenticators, which are actually digital keychains identified by unique IDs.
        
        These keychains contain both public keys, which can be freely shared, and their corresponding private keys, protected by passphrases, which must be kept hidden.
        
        Authenticators can be stored in your user profile or in a custom folder, especially at the root of removable devices.
        
        You can initialize new authenticators from scratch, import/export them from/to ZIP archives, or check their integrity by providing their passphrases.
        
        Note that if you destroy an authenticator and all its exported ZIP archives, the WitnessAngel recordings which used it as a trusted third party might not be decryptable anymore (unless they used a shared secret with other trusted third parties).
                 This page allows to publish the PUBLIC part of an authenticator to a remote Witness Angel Gateway, so that other users may import it to secure their recordings.
        
        For now, a published authenticator can't be modified or deleted.
        
        In case of incoherences between the keys locally and remotely stored, errors are displayed here.
         (Owner: {trustee_owner}) Abnormal error caught: %s Add a passphrase All authentication data from folder %s has been removed. Already existing passphrase %s An inconsistency has been detected between the local and remote authenticator. Are you sure you want to remove %s key guardian(s)? Authenticator ID Authenticator archive exported to %s Authenticator archive unpacked from %s, its integrity has not been checked though. Authenticator creation page Authenticator does not exist Authenticator has been imported successfully Authenticator initialized Authenticator management page Authenticator not initialized Authenticator publishing Authenticator: Back Back to home Badly formed hexadecimal UUID string Beware, this might make encrypted data using these keys impossible to decrypt. Camera url: {camera_url} Cancel Check Check passphrase Checkup result: %s Close Configuration errors prevent recording Confirm Container decryption confirmation Container decryption page Container deletion confirmation Container storage is invalid Container storage: {cryptainer_dir} Containers Containers are kept for {max_cryptainer_age_day} day(s) Control Recorder Create Authenticator Custom location Decrypt Decryption process Delete Deletion is over Destroy Destroy authenticator Do you want to import the private keys (passphrase-protected) as well? Drive: {drive} ({label}) Each container stores {video_recording_duration_mn} mn(s) of video Enter the ID of the authenticator: Enter the passphrase to decrypt the selected containers: Error calling method, already existing Error calling method, check the server url Error querying gateway server, please check its url Export Export authenticator Export successful Failure Found Gateway url: {wagateway_url} Help Import Import from USB Import from Web Import keys from USB drives Import keys from web gateway Import successful Initialization successfully completed. Initialize Invalid authenticator data in %s Invalid container storage: "{cryptainer_dir}" Key Guardian %s Key Guardians Key Guardians used: Key guardian removal confirmation Key guardian: {trustee_status} Key n° {index}, {key_algo} {keychain_uid}, private keys: {private_key_present_str}
 Keypairs successfully tested: %s Keypairs tested: {keypair_count}
Missing private keys: {missing_private_keys}
Wrong passphrase for keys:  {undecodable_private_keys} Language Manage Authenticators Missing key(s): {trustee_keys_missing} NOT PUBLISHED NOT found NOT set No No connected authentication devices found No containers found No containers selected No imported authentication device found No information available No initialized authentication devices found No valid location selected N° {index}: {cryptainer_name} Operation failed, check logs. PUBLISHED Passphrase Passphrase doesn't match any relevant private key Passphrase hint Passphrase must be at least %s characters long. Passphrase: {passphrase_status} Path: %s Please enter a username, passphrase and passphrase hint. Please select a folder Please select an authenticator folder Please select an authenticator location Please select containers to decrypt Please select containers to delete Please select key guardians to remove Please select the key guardians used to secure recordings Please wait, initialization might take a few minutes. Provide this ID to users wanting to rely on you as a Key Guardian Publish Publish authenticator Refresh Refreshed authenticator locations Refreshed imported authenticators Remote authenticator status has been updated Reset background service Sanity check Selected folder is invalid
Path: %s Set Settings Size: {size}, Filesystem: {filesystem} Some configuration changes might only apply at next recording restart Start Recording Stop Recording Stored inside system disk Success Summary of concerned key guardians Test integrity and passphrase of authenticator The exported archive should be kept in a secure place. The local authenticator does not exist in the remote repository. The remote authenticator is up to date. User Profile User name User {keystore_owner}, id {keystore_uid} Validation error View and manage encrypted containers Wrong camera url: "{camera_url}" Wrong gateway url: '{wagateway_url}' Yes no name {foreign_keystore_count} new authenticators imported, {already_existing_keystore_count} updated, {corrupted_keystore_count} skipped because corrupted {keyguardian_count} key guardian(s) configured, {keyguardian_threshold} of which necessary for decryption {trustee_type} {keystore_uid} Project-Id-Version: WitnessAngelGuilib
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2022-03-05 21:17+0200
Last-Translator: Pascal <pythoniks@gmail.com>
Language-Team: Nothing
Language: fr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n > 1);
X-Generator: Virtaal 0.7.1
                         Passerelle : {gateway}
                        Statut distant : {status}
                        Message : {message}
                        
                        ID authentifieur : {keystore_uid}
                                           Détails d'erreurs :
                           Clés en excès côté distant : {exceeding_keys_in_remote}
                           Clés manquantes côté distant : {missing_keys_in_remote}
                                       Chemin : {authenticator_dir}
                    ID : {keystore_uid}
                    Utilisateur : {keystore_owner}
                    Indice de phrase secrète : {keystore_passphrase_hint}         Sur cette page, vous pouvez initialiser un authentifieur dans un dossier vide ; cet authentifieur consiste en réalité en des fichiers de métadonnées, ainsi qu'en un ensemble de paires de clés asymétriques.
        
        Pour procéder, vous devez entrer votre nom d'utilisateur ou pseudo, une longue phrase secrète (par exemple, composée de 4 mots différents), et un indice public pour vous aider à vous souvenir de votre phrase secrète plus tard.
        
        Vous devez conserver votre phrase secrète en lieu sûr (dans un gestionnaire de mots de passe numérique, sur un papier dans un coffre-fort...), car si vous oubliez l'un de ses aspects (majuscules/minuscules, accents, espaces...), il n'y a aucun moyen de la récupérer.
                 Sur cette page, vous pouvez gérer vos authentifieurs, qui sont en fait des trousseaux de clés numériques identifiés par des ID uniques.
        
        Ces trousseaux contiennent à la fois des clés publiques, qui peuvent être partagées librement, et les clés privées correspondantes, protégées par des phrases secrètes, qui doivent rester cachées.
        
        Les authentifieurs peuvent être stockés dans votre profil utilisateur ou dans un dossier personnalisé, notamment à la racine des périphériques amovibles.
        
        Vous pouvez initialiser de nouveaux authentifieurs à partir de zéro, les importer/exporter depuis/vers des archives ZIP, ou vérifier leur intégrité en fournissant leurs phrases secrètes.
        
        Notez que si vous détruisez un authentifieur et toutes ses archives ZIP exportées, les enregistrements WitnessAngel qui l'utilisaient en tant que tiers de confiance risquent de ne plus pouvoir être déchiffrés (à moins qu'ils n'aient utilisé un secret partagé avec d'autres tiers de confiance).         Cette page permet de publier la partie PUBLIC d'un authentifiant sur une passerelle Witness Angel distante, afin que d'autres utilisateurs puissent l'importer pour sécuriser leurs enregistrements.
        
        Pour l'instant, un authentifiant publié ne peut pas être modifié ou supprimé.
        
        En cas d'incohérences entre les clés stockées localement et à distance, des erreurs sont affichées ici. (Propriétaire : {trustee_owner}) Erreur anormale détectée : %s Ajouter une phrase secrète Toutes les données d'authentifieur du dossier %s ont été supprimées. Phrase secrète déjà existante %s Une incohérence a été détectée entre l'authentifieur local et distant Êtes-vous sûr de vouloir supprimer %s gardien(s) de clé ID d'authentifieur : L'archive de l'authentifieur a été exportée vers %s L'archive d'authentifieur a été décompressée depuis %s, son intégrité n'a cependant pas été vérifiée. Page de création d'authentifieur Authentifieur non existant L'authentifieur a été importé avec succès Authentifieur initialisé Page de gestion des authentifieurs Authentifieur non initialisé Publication de l'authentifieur Authentifieur : Retour Retour Chaîne UUID hexadécimale mal formée Attention, cela peut rendre impossible le déchiffrement des données chiffrées utilisant ces clés. Url de la caméra : {camera_url} Annuler Vérifier Vérifier la phrase secrète Résultat du contrôle : %s Fermer Des erreurs de configuration empêchent l'enregistrement Confirmer Confirmation de déchiffrement de conteneur Page de déchiffrement de conteneurs Confirmation de suppression de conteneur Le dépôt de conteneurs est invalide Stockage des conteneurs : {cryptainer_dir} Conteneurs Les conteneurs sont gardés {max_cryptainer_age_day} jour(s) Contrôler Enregistreur Créer un Authentifieur Emplacement personnalisé Déchiffrer Processus de déchiffrement Supprimer Destruction terminée Détruire Détruire l'authentifieur Voulez-vous aussi importer les clés privées (protégées par phrase secrète) ? Disque : {drive} ({label}) Chaque conteneur stocke {video_recording_duration_mn} mn(s) de vidéo Entrez l'ID de l'authentifieur : Entrez la phrase secrète pour déchiffrer les conteneurs sélectionnés. Erreur à l'appel de la méthode, déjà existant Erreur à l'appel de la méthode, vérifier l'url du serveur Erreur lors de l'appel au serveur gateway, veuillez vérifier son url Exporter Exporter l'authentifieur Exportation réussie Échec Trouvé Url de la passerelle : {wagateway_url} Aide Importer Import depuis USB Import depuis Web Import de clés depuis les stockages USB Import de clés depuis la passerelle web Importation réussie Initialisation complétée avec succès. Initialiser Données d'authentifieur invalides dans %s Stockage des conteneurs invalide : {cryptainer_dir} Gardien de Clés %s Gardiens des Clés Gardiens des Clés utilisés : Confirmation de suppression de gardiens de clé Gardien des clés : {trustee_status} Clé n° {index}, {key_algo} {keychain_uid}, clés privées: {private_key_present_str}
 Paires de clés testées avec succès : %s Paires de clés testées : {keypair_count}
Clés privées manquantes : {missing_private_keys}
Mauvaise phrase secrète pour les clés :  {undecodable_private_keys} Langue Gérer les Authentifieurs Clé(s) manquante(s) : {trustee_keys_missing} NON PUBLIÉ NON trouvé NON renseigné Non Aucun périphérique d'authentification trouvé Aucun conteneur trouvé Aucun conteneur sélectionné Aucun périphérique d'authentification importé trouvé Aucune information disponible Aucun périphérique d'authentification initialisé trouvé Aucun emplacement valide sélectionné N° {index}: {cryptainer_name} Opération échouée, vérifiez les logs. PUBLIÉ Phrase secrète La phrase secrète ne correspond à aucune clé privée pertinente Indice de phrase secrète La phrase secrète doit faire au moins %s caractères de long. Phrase secrète : {passphrase_status} Chemin : %s Veuillez entrer un nom d'utilisateur, une phrase secrète et son indice. Veuillez sélectionner un dossier Veuillez sélectionner un dossier d'authentifieur Veuillez sélectionner un emplacement d'authentifieur Veuillez sélectionner les conteneurs à déchiffrer Veuillez sélectionner les conteneurs à supprimer Veuillez sélectionner les gardiens de clé à supprimer Veuillez sélectionner les gardiens de clés utilisés pour sécuriser les enregistrements Veuillez attendre, l'initialisation peut prendre quelques minutes. Fournissez cet ID aux utilisateurs désirant vous ajouter comme Gardien de Clés Publier Publier l'authentifieur Rafraîchir Emplacements d'authentifieurs rafraichis Authentifieurs importés rafraîchis Le statut de l'authentifieur distant a été actualisé Réinitialiser le service en fond Contrôle d'intégrité Le dossier sélectionné est invalide
Chemin : %s Renseigné Paramètres Taille : {size}, Format : {filesystem} Certains changements de configuration pourraient ne s'appliquer qu'au redémarrage de l'enregistrement Lancer Enregistrement Arrêter Enregistrement Stocké dans le disque système Succès Résumé des gardiens de clé concernés Tester l'intégrité et la phrase secrète de l'authentifieur L'archive exportée doit être gardée en lieu sûr. L'authentifieur local n'existe pas dans le dépôt distant. L'authentifieur distant est à jour. Profil Utilisateur Utilisateur Utilisateur {keystore_owner}, id {keystore_uid} Erreur de validation Voir et gérer les conteneurs chiffrés Mauvaise url de caméra : "{camera_url}" Mauvaise url de passerelle : '{wagateway_url}' Oui sans nom {foreign_keystore_count} nouveaux authentifieurs importé(s) avec succès, {already_existing_keystore_count} mis à jour, {corrupted_keystore_count} ignoré(s) car corrompu(s) {keyguardian_count} gardien(s) de clés configuré(s), dont {keyguardian_threshold} nécessaire(s) pour le déchiffrement {trustee_type} {keystore_uid} 