import java.util.Locale;
import java.util.ResourceBundle;

public class TestTranslation {
    public static void main(String[] args) {
        Locale frLocale = Locale.FRENCH;

        try {
            ResourceBundle bundle = ResourceBundle.getBundle("messages", frLocale);

            System.out.println("Testing translation keys:");
            System.out.println("---");

            String[] keys = {
                "quizEditor.selectQuiz",
                "quizEditor.questionNumber",
                "quizEditor.title",
                "quizEditor.difficultyLevel",
                "quizEditor.updateFile",
                "quizEditor.previous",
                "quizEditor.next",
                "menu.editquizzes"
            };

            for (String key : keys) {
                try {
                    String value = bundle.getString(key);
                    System.out.println("✅ '" + key + "' = '" + value + "'");
                } catch (Exception e) {
                    System.out.println("❌ '" + key + "' NOT FOUND - " + e.getMessage());
                }
            }

        } catch (Exception e) {
            System.out.println("ERROR loading bundle: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

