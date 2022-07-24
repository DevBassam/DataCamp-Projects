--Task 1: Instructions
--Find names that have been given to over 5,000 babies of either sex every year for the 101 years from 1920 through 2020;
--recall that names only show up in our dataset when at least 5,000 babies have been given that name in a year.

SELECT FIRST_NAME ,SUM(NUM) 
FROM BABY_NAMES
GROUP BY FIRST_NAME
HAVING COUNT(YEAR) = 101
ORDER BY 2 DESC


--Task 2: Instructions
--Classify each name's popularity according to the number of years that the name appears in the dataset.

SELECT FIRST_NAME,SUM(NUM),
       CASE WHEN COUNT(FIRST_NAME) > 80 THEN 'Classic'
        WHEN COUNT(FIRST_NAME) > 50 THEN 'Semi-classic'
        WHEN COUNT(FIRST_NAME) > 20 THEN 'Semi-trendy'
        ELSE 'Trendy'END AS POPULARITY_TYPE
FROM BABY_NAMES
GROUP BY FIRST_NAME
ORDER BY FIRST_NAME ASC


--Task 3: Instructions
--Let's take a look at the ten highest-ranked American female names in our dataset.

SELECT RANK() OVER(ORDER BY SUM(NUM) DESC) AS NAME_RANK,
       FIRST_NAME,SUM(NUM)
FROM BABY_NAMES
WHERE SEX = 'F'
GROUP BY FIRST_NAME
ORDER BY NAME_RANK 
LIMIT 10


--Task 4: Instructions
--Return a list of first names which meet this friend's baby name criteria.

SELECT FIRST_NAME FROM BABY_NAMES
WHERE SEX = 'F' AND YEAR > 2015 AND FIRST_NAME LIKE '%a'
GROUP BY FIRST_NAME
ORDER BY SUM(NUM) DESC


--Task 5: Instructions
--Find the cumulative number of babies named Olivia over the years since the name first appeared in our dataset.

SELECT YEAR, FIRST_NAME, NUM,
       SUM(NUM) OVER (ORDER BY year) AS cumulative_olivias
FROM BABY_NAMES
WHERE FIRST_NAME = 'Olivia'
ORDER BY YEAR

--Task 6: Instructions
--Write a query that selects the year and the maximum num of babies given any male name in that year.

SELECT YEAR,MAX(NUM) AS MAX_NUM
FROM BABY_NAMES
WHERE SEX = 'M'
GROUP BY YEAR

--Task 7: Instructions
--Using the previous task's code as a subquery,
--look up the first_name that corresponds to the maximum number of babies given a specific male name in a year.

SELECT B.YEAR, B.FIRST_NAME, B.NUM
FROM BABY_NAMES AS B
INNER JOIN(
    SELECT YEAR,MAX(NUM) AS MAX_NUM
    FROM BABY_NAMES
    WHERE SEX = 'M'
    GROUP BY YEAR) AS MAX_FIRST_NAME
ON B.NUM = MAX_FIRST_NAME.MAX_NUM 
    AND B.YEAR = MAX_FIRST_NAME.YEAR
ORDER BY YEAR DESC


--Task 8: Instructions
--Return a list of first names that have been the top male first name in any year along 
--with a count of the number of years that name has been the top name.

WITH M AS(
SELECT B.YEAR, B.FIRST_NAME, B.NUM
FROM BABY_NAMES AS B
INNER JOIN(
    SELECT YEAR,MAX(NUM) AS MAX_NUM
    FROM BABY_NAMES
    WHERE SEX = 'M'
    GROUP BY YEAR) AS MAX_FIRST_NAME
ON B.NUM = MAX_FIRST_NAME.MAX_NUM 
    AND B.YEAR = MAX_FIRST_NAME.YEAR
ORDER BY YEAR DESC
)

SELECT FIRST_NAME,COUNT(YEAR) AS count_top_name
FROM M
GROUP BY FIRST_NAME
ORDER BY COUNT(YEAR) DESC