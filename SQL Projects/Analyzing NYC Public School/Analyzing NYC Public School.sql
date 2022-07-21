--Task 1: Instructions
--Select all columns from schools.
--Limit the output to 10 schools.

SELECT * 
FROM SCHOOLS
LIMIT 10

--Task 2: Instructions
--Count the number of schools not reporting the percentage of students tested and the total number of schools in the database.
--Select the number of schools minus the number of entries for percent_tested, aliasing as num_tested_missing.
--Count how many schools are in the database, aliasing as num_schools.

SELECT COUNT(SCHOOL_NAME)-COUNT(PERCENT_TESTED) AS num_tested_missing , 
        COUNT(SCHOOL_NAME) AS num_schools
FROM SCHOOLS 

--Task 3: Instructions
--Find how many unique schools there are based on building code.
--Count the number of unique values for building_code, aliasing as num_school_buildings.

SELECT COUNT(DISTINCT BUILDING_CODE) AS num_school_buildings
FROM SCHOOLS

--Task 4: Instructions
--Filter the database for all schools with math scores of at least 640.
--Select the name of the school and average_math, filtering for rows with a score more than or equal to 640.
--Sort by average_math in descending order.

SELECT SCHOOL_NAME,AVERAGE_MATH
FROM SCHOOLS
WHERE AVERAGE_MATH >= 640
ORDER BY AVERAGE_MATH DESC

--Task 5: Instructions
--Find the lowest average reading score.
--Select the lowest value for average_reading, aliased as lowest_reading.

SELECT MIN(AVERAGE_READING) AS lowest_reading
FROM SCHOOLS

--Task 6: Instructions
--Filter the database for the top-performing school, as measured by average writing scores.
--Select school_name and the largest value for average_writing, aliased as max_writing.
--Group the results by school_name.
--Sort results by max_writing in descending order.
--Limit the output to one result.

SELECT SCHOOL_NAME,MAX(AVERAGE_WRITING) AS max_writing
FROM SCHOOLS
GROUP BY SCHOOL_NAME
ORDER BY MAX_WRITING DESC
LIMIT 1

--Task 7: Instructions
--Create total SAT scores and find the top 10 best schools.
--Select school_name, and the total of average_math, average_reading, and average_writing, aliased as average_sat.
--Group by school name.
--Sort by average_sat in descending order.
--Return the top 10 schools.

SELECT SCHOOL_NAME,(AVERAGE_MATH+AVERAGE_READING+AVERAGE_WRITING) AS average_sat
FROM SCHOOLS
GROUP BY SCHOOL_NAME
ORDER BY AVERAGE_SAT DESC
LIMIT 10

--Task 8: Instructions
--Find out how NYC SAT performance varies by borough.
--Select borough and a count of all schools, aliased as num_schools.
--Select the sum of average_math, average_reading, and average_writing, divided by a count of all schools, aliasing as average_borough_sat.
--Use a function to aggregate the results by borough.
--Sort the results by average_borough_sat in descending order.

SELECT BOROUGH,COUNT(SCHOOL_NAME) AS num_schools,
     (SUM(AVERAGE_MATH)+SUM(AVERAGE_READING)+SUM(AVERAGE_WRITING))/COUNT(SCHOOL_NAME) AS average_borough_sat
FROM SCHOOLS
GROUP BY BOROUGH
ORDER BY average_borough_sat DESC

--Task 9: Instructions
--Find the top five best schools in Brooklyn by math score.
--Select school_name and average_math.
--Filter for rows where the borough is 'Brooklyn'.
--Aggregate by school_name.
--Sort by average_math in descending order, and display the top five results.

SELECT SCHOOL_NAME,AVERAGE_MATH
FROM SCHOOLS
WHERE BOROUGH = 'Brooklyn'
ORDER BY 2 DESC
LIMIT 5