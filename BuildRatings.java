import org.openqa.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import java.util.*;
import java.sql.*;

public class BuildRatings {
	public static void main(String[] args) {
		float rating;
		String res_id,res_name,res_url,user_id;
		String sql = "insert into restaurant_ratings (user_id,res_id,res_name,rating) values (?,?,?,?)";
		try{
			System.setProperty("webdriver.chrome.driver","/Users/anuyogrohilla/Downloads/chromedriver");
			WebDriver driver = new ChromeDriver();
			Connection myConn = DriverManager.getConnection("jdbc:mysql://localhost:3306/restaurants_data","root","mysql");   // Connection object to retrieve data from restaurants_complete table
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/restaurants_data","root","mysql");  // Connection object to insert data into restaurant_ratings table
			PreparedStatement preparedStmt = conn.prepareStatement(sql);
			Statement myStmt = myConn.createStatement();
			ResultSet rs = myStmt.executeQuery("select * from restaurants_complete where id>=1 and id<=5");  // provide start id and and end id accordingly
			while(rs.next()){
				res_id = rs.getString("res_id");
				res_name = rs.getString("res_name");
				res_url = rs.getString("res_url");
				driver.get(res_url);
				try{
					Thread.sleep(1000);
				}
				catch(Exception e){
					e.printStackTrace();
				}
				while(true){
					try{
						WebElement load = driver.findElement(By.cssSelector("div.load-more.bold.ttupper.tac.cursor-pointer.fontsize2"));
						load.click();
						try{
							Thread.sleep(1000);
						}
						catch(Exception e){
							e.printStackTrace();
						}
					}
					catch(Exception e){
						break;
					}
				}
				
				List<WebElement> users = driver.findElements(By.cssSelector("div.header.nowrap.ui.left"));
				List<WebElement> userInfo = driver.findElements(By.cssSelector("span.grey-text.fontsize5.nowrap"));
				List<WebElement> ratings = driver.findElements(By.cssSelector("div.rev-text.mbot0"));
				for(int i=0;i<users.size();i++){
					user_id = users.get(i).getText() + " " + userInfo.get(i).getText();
					rating = Float.valueOf(ratings.get(i).findElement(By.className("ttupper")).getAttribute("aria-label").substring(6)).floatValue();
					preparedStmt.setString(1,user_id);
					preparedStmt.setString(2,res_id);
					preparedStmt.setString(3,res_name);
					preparedStmt.setFloat(4,rating);
					preparedStmt.executeUpdate();
				}
				try{
					Thread.sleep(1000);
				}
				catch(Exception e){
					e.printStackTrace();
				}
			}
			myConn.close();
			conn.close();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

}
