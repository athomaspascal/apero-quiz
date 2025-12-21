package com.quizz.core.entity;

import jakarta.persistence.*;
import org.jspecify.annotations.Nullable;

@Entity
@Table(name = "users")
public class User {

    public static final int NAME_MAX_LENGTH = 200;
    public static final int EMAIL_MAX_LENGTH = 255;
    public static final int TELEPHONE_MAX_LENGTH = 20;
    public static final int PASSWORD_MAX_LENGTH = 255;


    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "user_id")
    private Long id;

    @Column(name = "name", nullable = false, length = NAME_MAX_LENGTH)
    private String name = "";

    @Column(name = "email", nullable = false, unique = true, length = EMAIL_MAX_LENGTH)
    private String email = "";

    @Column(name = "telephone", length = TELEPHONE_MAX_LENGTH)
    private String telephone = "";

    @Column(name = "password", length = PASSWORD_MAX_LENGTH)
    private String password = "";

    @Column(name = "oauth_provider", length = 50)
    private String oauthProvider;

    @Column(name = "oauth_provider_id", length = 255)
    private String oauthProviderId;

    @Enumerated(EnumType.STRING)
    @Column(name = "gender", length = 10)
    private Gender gender;

    @Lob
    @Basic(fetch = FetchType.LAZY)
    @Column(name = "photo_bytes")
    private byte[] photoBytes;

    @Column(name = "is_public", nullable = false)
    private boolean isPublic = false;

    @Column(name = "is_admin", nullable = false)
    private boolean isAdmin = false;

    public User() { // To keep Hibernate happy
    }

    public User(String name, String email, String telephone, String password) {
        setName(name);
        setEmail(email);
        setTelephone(telephone);
        setPassword(password);
    }

    public User(String name, String email, String telephone, String password, Gender gender) {
        setName(name);
        setEmail(email);
        setTelephone(telephone);
        setPassword(password);
        setGender(gender);
    }

    public @Nullable Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if (name.length() > NAME_MAX_LENGTH) {
            throw new IllegalArgumentException("Name length exceeds " + NAME_MAX_LENGTH);
        }
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        if (email.length() > EMAIL_MAX_LENGTH) {
            throw new IllegalArgumentException("Email length exceeds " + EMAIL_MAX_LENGTH);
        }
        this.email = email;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setTelephone(String telephone) {
        if (telephone.length() > TELEPHONE_MAX_LENGTH) {
            throw new IllegalArgumentException("Telephone length exceeds " + TELEPHONE_MAX_LENGTH);
        }
        this.telephone = telephone;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        if (password != null && password.length() > PASSWORD_MAX_LENGTH) {
            throw new IllegalArgumentException("Password length exceeds " + PASSWORD_MAX_LENGTH);
        }
        this.password = password;
    }

    public String getOauthProvider() {
        return oauthProvider;
    }

    public void setOauthProvider(String oauthProvider) {
        this.oauthProvider = oauthProvider;
    }

    public String getOauthProviderId() {
        return oauthProviderId;
    }

    public void setOauthProviderId(String oauthProviderId) {
        this.oauthProviderId = oauthProviderId;
    }

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
    }

    public byte[] getPhotoBytes() {
        return photoBytes;
    }

    public void setPhotoBytes(byte[] photoBytes) {
        this.photoBytes = photoBytes;
    }

    public boolean isPublic() {
        return isPublic;
    }

    public void setPublic(boolean aPublic) {
        isPublic = aPublic;
    }

    public boolean isAdmin() {
        return isAdmin;
    }

    public void setAdmin(boolean admin) {
        isAdmin = admin;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null || !getClass().isAssignableFrom(obj.getClass())) {
            return false;
        }
        if (obj == this) {
            return true;
        }

        User other = (User) obj;

        return id != null && id.equals(other.getId());
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : super.hashCode();
    }
}
