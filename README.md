# ESN Mentor

Projekt polega na zaimplementowaniu systemu doboru mentorów dla studentów w ramach programu ESN. Bazuje on na frameworku Django oraz bazie danych PostgreSQL.


# Działanie aplikacji

System działa na następujących zasadach:

1. Użytkownik rejestruje się w systemie, podając swoje dane oraz określając typ konta (student, mentor, admin). W przypadku mentorów, określana jest także liczba miejsc, które mają dostępne dla mentorowania.
2. Użytkownik wypełnia formularz, na który składa się zestaw pytań z modelu Question. Odpowiedzi na te pytania są zapisywane w modelu FormAnswer, a konkretne odpowiedzi na pytania są zapisywane w modelu Answer.
3. Na podstawie wypełnionych formularzy oraz dostępności mentorów, studenci wysyłają prośbę o udzielenie im mentoringu. Mentorzy wybierają, ile studentów chcą wziąć pod swoją opiekę i system blokuje możliwość "przygarnięcia" większej ilości studentów. Mentorzy dostają prośby wysyłane przez studentów i jet akceptują lub odrzucają. Wybór jest reprezentowany przez model [MentoringChoice](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L64), który przechowuje informacje o mentorze, studencie i statusie wyboru (akceptowany, odrzucony, oczekujący).


# Schemat bazy danych

Nasz projekt korzysta z następujących modeli, które reprezentują tabele w naszej bazie danych:

* [User](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L19): Reprezentuje użytkownika systemu.
* [FormAnswer](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L44): Przechowuje odpowiedzi na pytania formularza od użytkowników.
* [Question](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L49): Reprezentuje pytania w formularzu.
* [Answer](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L58): Reprezentuje odpowiedzi na pytania w formularzu.
* [MentoringChoice](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L64): Przechowuje wybory mentora dokonane przez studentów.

Relacje między tabelami są następujące:

* User posiada relację One-to-Many z MentoringChoice jako student i mentor.
* FormAnswer ma relację One-to-One z User.
* Answer ma relację One-to-One z FormAnswer i Question.

Szczegółowy schemat bazy danych można znaleźć w pliku [models.py](https://github.com/sxevush/bazydanych-esn-mentor/blob/main/mentor_app/models.py).


# Modele

Szczegółowe informacje o modelach można znaleźć w pliku [models.py](https://github.com/sxevush/bazydanych-esn-mentor/blob/main/mentor_app/models.py)


## User
Model [User](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L19) to niestandardowy model użytkownika Django, który dodaje dodatkowe pole account_type, mentorships_left oraz modyfikuje pole email, ustawiając je jako unikalne oraz jako główne pole do logowania. Dodatkowo, model posiada pola first_name, last_name, username, is_active, is_staff, is_superuser które są standardowymi polami modelu użytkownika Django.

* account_type to pole typu CharField i definiuje typ konta użytkownika. Możliwe opcje to: 'student', 'mentor', 'admin'.
* mentorships_left to pole typu IntegerField określające ilość dostępnych miejsc dla danego mentora.
* CustomUserManager to menedżer modelu User służący do tworzenia nowych instancji użytkowników oraz super użytkowników.

## FormAnswer
Model [FormAnswer](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L44) reprezentuje odpowiedzi na pytania formularza. Składa się z dwóch pól: user (relacja OneToOne z modelem User) oraz created_at (czas utworzenia).

## Question
Model [Question](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L49) reprezentuje pytania w formularzu. Składa się z dwóch pól: question (pytanie) oraz user_group (typ użytkownika, do którego jest skierowane pytanie - 'student' lub 'mentor').

## Answer
Model [Answer](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L58) reprezentuje odpowiedzi na pytania w formularzu. Składa się z trzech pól: question (pytanie), answer (odpowiedź) oraz form (klucz obcy do FormAnswer).

## MentoringChoice
Model [MentoringChoice](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/models.py#L64) reprezentuje wybór mentora przez studenta. Składa się z trzech pól: mentor (klucz obcy do User, reprezentuje mentor), student (klucz obcy do User, reprezentuje studenta), status (status wyboru mentora - 'accepted', 'rejected', 'pending').


# Formularze

Szczegółowe informacje o formularzach można znaleźć w pliku [forms.py](https://github.com/sxevush/bazydanych-esn-mentor/blob/main/mentor_app/forms.py)

* [RegistrationForm](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/forms.py#L9), [LoginForm](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/forms.py#L15) oraz [ProfileForm](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/forms.py#L21) to formularze do rejestracji, logowania i edycji profilu użytkownika.

* [FormAnswersForm](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/forms.py#L27) jest formularzem do zbierania odpowiedzi użytkowników. W konstruktorze formularza, zapytania są pobierane na podstawie grupy użytkowników. Na podstawie tych pytań, tworzone są odpowiednie pola formularza. Metoda save tworzy nową instancję FormAnswer oraz Answer dla każdej odpowiedzi.

* [MentorSelectionForm](https://github.com/sxevush/bazydanych-esn-mentor/blob/dae0734dc2cda1d9687e03f657d5044825d022aa/mentor_app/forms.py#L53) jest formularzem do wyboru mentora przez studenta. W konstruktorze formularza, użytkownicy są pobierani z wykluczeniem tych, którzy nie mają dostępnych miejsc na mentorowania (`mentorships_left=0`). Metoda save tworzy nową instancję MentoringChoice.


# Widoki

Szczegółowe informacje o widokach można znaleźć w pliku [views.py](https://github.com/sxevush/bazydanych-esn-mentor/blob/main/mentor_app/views.py)

* RegistrationView - Umożliwia użytkownikowi zarejestrowanie się w systemie. Odwołuje się do funkcji register() w views.py i URL /register/.
* LoginView - Służy do logowania użytkowników. Odwołuje się do funkcji log_in() w views.py i URL /login/.
* LogoutView - Pozwala użytkownikowi na wylogowanie się z systemu. Odwołuje się do funkcji log_out() w views.py i URL /logout/.
* PanelView - Wyświetla panel użytkownika. Odwołuje się do funkcji panel() w views.py i URL /panel/.
* EditProfileView - Umożliwia edycję profilu użytkownika. Odwołuje się do funkcji edit_profile() w views.py i URL /edit_profile/.
* UserProfileView - Wyświetla profil konkretnego użytkownika. Odwołuje się do funkcji profile_view() w views.py i URL /profile/<int:id>/.
* FormAnswerCreationView - Umożliwia użytkownikowi uzupełnienie formularza i zapisanie odpowiedzi. Odwołuje się do funkcji form_view() w views.py i URL /form/.
* MentorSelectionView - Pozwala studentom na wybór mentora. Odwołuje się do funkcji mentor_selection_view() w views.py i URL /mentor_select/.
* MentorChoicesView - Umożliwia mentorowi przeglądanie wyborów mentora dokonanych przez studentów oraz ich akceptację lub odrzucenie. Odwołuje się do funkcji accept_students_view() w views.py i URL /accept_students/.
* AddQuestionView - Umożliwia dodanie nowego pytania do formularza. Odwołuje się do funkcji add_question_view() w views.py i URL /add_question/.
* MentorshipEditView - Umożliwia mentorowi edycję dostępnych miejsc do mentorowania. Odwołuje się do funkcji edit_mentorships() w views.py i URL /mentorships_left/.
* SuccessView - Wyświetla strony z potwierdzeniem po poprawnej akcji użytkownika. Odwołuje się do funkcji success() w views.py i URL /success/.
* AlreadyFilledView - Wyświetla informację, że formularz został już wypełniony. Odwołuje się do funkcji already_filled() w views.py i URL /already_filled/.
