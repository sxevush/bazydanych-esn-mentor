# Dokumentacja projektu Mentor-Matching ESN

Projekt polega na zaimplementowaniu systemu doboru mentorów dla studentów w ramach programu ESN. Bazuje on na frameworku Django oraz bazie danych PostgreSQL.

# Schemat bazy danych

Nasz projekt korzysta z następujących modeli, które reprezentują tabele w naszej bazie danych:

* User: Reprezentuje użytkownika systemu.
* FormAnswer: Przechowuje odpowiedzi na pytania formularza od użytkowników.
* Question: Reprezentuje pytania w formularzu.
* Answer: Reprezentuje odpowiedzi na pytania w formularzu.
* MentoringChoice: Przechowuje wybory mentora dokonane przez studentów.

Relacje między tabelami są następujące:

* User posiada relację One-to-Many z MentoringChoice jako student i mentor.
* FormAnswer ma relację One-to-One z User.
* Answer ma relację One-to-One z FormAnswer i Question.
Szczegółowy schemat bazy danych można znaleźć w pliku [models.py](https://github.com/sxevush/bazydanych-esn-mentor/blob/main/mentor_app/models.py).

# Modele

## User
Model User to niestandardowy model użytkownika Django, który dodaje dodatkowe pole account_type, mentorships_left oraz modyfikuje pole email, ustawiając je jako unikalne oraz jako główne pole do logowania. Dodatkowo, model posiada pola first_name, last_name, username, is_active, is_staff, is_superuser które są standardowymi polami modelu użytkownika Django.

* account_type to pole typu CharField i definiuje typ konta użytkownika. Możliwe opcje to: 'student', 'mentor', 'admin'.
* mentorships_left to pole typu IntegerField określające ilość dostępnych miejsc dla danego mentora.
* CustomUserManager to menedżer modelu User służący do tworzenia nowych instancji użytkowników oraz super użytkowników.

## FormAnswer
Model FormAnswer reprezentuje odpowiedzi na pytania formularza. Składa się z dwóch pól: user (relacja OneToOne z modelem User) oraz created_at (czas utworzenia).

## Question
Model Question reprezentuje pytania w formularzu. Składa się z dwóch pól: question (pytanie) oraz user_group (typ użytkownika, do którego jest skierowane pytanie - 'student' lub 'mentor').

## Answer
Model Answer reprezentuje odpowiedzi na pytania w formularzu. Składa się z trzech pól: question (pytanie), answer (odpowiedź) oraz form (klucz obcy do FormAnswer).

## MentoringChoice
Model MentoringChoice reprezentuje wybór mentora przez studenta. Składa się z trzech pól: mentor (klucz obcy do User, reprezentuje mentor), student (klucz obcy do User, reprezentuje studenta), status (status wyboru mentora - 'accepted', 'rejected', 'pending').

# Formularze

* RegistrationForm, LoginForm, ProfileForm
RegistrationForm, LoginForm oraz ProfileForm to formularze do rejestracji, logowania i edycji profilu użytkownika.

* FormAnswersForm
FormAnswersForm jest formularzem do zbierania odpowiedzi użytkowników. W konstruktorze formularza, zapytania są pobierane na podstawie grupy użytkowników. Na podstawie tych pytań, tworzone są odpowiednie pola formularza. Metoda save tworzy nową instancję FormAnswer oraz Answer dla każdej odpowiedzi.

* MentorSelectionForm
MentorSelectionForm jest formularzem do wyboru mentora przez studenta. W konstruktorze formularza, użytkownicy są pobierani z wykluczeniem tych, którzy nie mają dostępnych miejsc na mentorowania (`mentorships_left=0`). Metoda save tworzy nową instancję MentoringChoice.

# Widoki

Nasz projekt używa Django Class-Based Views do stworzenia odpowiednich widoków.

* RegistrationView - Umożliwia użytkownikowi zarejestrowanie się w systemie.
* LoginView - Służy do logowania użytkowników.
* ProfileView - Wyświetla profil użytkownika oraz umożliwia jego edycję.
* FormAnswersView - Umożliwia użytkownikowi uzupełnienie formularza i zapisanie odpowiedzi.
* MentorSelectionView - Pozwala studentom na wybór mentora.
* MentorChoicesView - Umożliwia mentorowi przeglądanie wyborów mentora dokonanych przez studentów oraz ich akceptację lub odrzucenie.
