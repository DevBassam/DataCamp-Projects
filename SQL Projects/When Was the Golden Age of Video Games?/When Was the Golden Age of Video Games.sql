-- Task1:
-- Select all information for the top ten best-selling games
-- Order the results from best-selling game down to tenth best-selling

SELECT * FROM GAME_SALES
ORDER BY GAMES_SOLD DESC
LIMIT 10

-- Task2:
-- Join games_sales and reviews
-- Select a count of the number of games where both critic_score and user_score are null

SELECT COUNT(GAME) FROM GAME_SALES
LEFT JOIN REVIEWS
USING(GAME)
WHERE CRITIC_SCORE IS NULL 
AND USER_SCORE IS NULL


-- Task3:
-- Select release year and average critic score for each year, rounded and aliased
-- Join the game_sales and reviews tables
-- Group by release year
-- Order the data from highest to lowest avg_critic_score and limit to 10 results

SELECT YEAR,ROUND(AVG(CRITIC_SCORE),2) AS avg_critic_score
FROM GAME_SALES
INNER JOIN REVIEWS
USING(GAME)
GROUP BY YEAR
ORDER BY avg_critic_score DESC
LIMIT 10

-- Task4:
-- Paste your query from the previous task; update it to add a count of games released in each year called num_games
-- Update the query so that it only returns years that have more than four reviewed games

SELECT YEAR,ROUND(AVG(CRITIC_SCORE),2) AS avg_critic_score,COUNT(GAME) AS num_games
FROM GAME_SALES
INNER JOIN REVIEWS
USING(GAME)
GROUP BY YEAR
HAVING COUNT(GAME) > 4
ORDER BY avg_critic_score DESC
LIMIT 10

-- Task5:
-- Select the year and avg_critic_score for those years that dropped off the list of critic favorites 
-- Order the results from highest to lowest avg_critic_score

SELECT YEAR,avg_critic_score FROM top_critic_years
EXCEPT
SELECT YEAR,avg_critic_score FROM top_critic_years_more_than_four_games
ORDER BY avg_critic_score DESC

-- Task6:
-- Select year, an average of user_score, and a count of games released in a given year, aliased and rounded
-- Include only years with more than four reviewed games; group data by year
-- Order data by avg_user_score, and limit to ten results

SELECT YEAR,ROUND(AVG(USER_SCORE),2) AS avg_user_score,COUNT(GAME) AS num_games
FROM GAME_SALES
INNER JOIN REVIEWS
USING(GAME)
GROUP BY YEAR
HAVING COUNT(GAME) > 4
ORDER BY avg_user_score DESC

-- Task7:
-- Select the year results that appear on both tables

SELECT YEAR FROM top_critic_years_more_than_four_games
INTERSECT
SELECT YEAR FROM top_user_years_more_than_four_games
LIMIT 10

-- Task8:
-- Select year and sum of games_sold, aliased as total_games_sold; order results by total_games_sold descending
-- Filter game_sales based on whether each year is in the list returned in the previous task

SELECT YEAR,SUM(GAMES_SOLD) AS total_games_sold
FROM GAME_SALES
WHERE YEAR IN (
            SELECT YEAR FROM top_critic_years_more_than_four_games
            INTERSECT
            SELECT YEAR FROM top_user_years_more_than_four_games)
GROUP BY YEAR
ORDER BY 2 DESC