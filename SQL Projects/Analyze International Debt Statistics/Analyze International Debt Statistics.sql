--Task1:

SELECT * FROM international_debt
LIMIT 10

--Task2:

SELECT 
    COUNT(DISTINCT country_name) AS total_distinct_countries
FROM international_debt;

--Task3:

SELECT DISTINCT indicator_code AS distinct_debt_indicators
FROM international_debt
ORDER BY distinct_debt_indicators

--Task4:

SELECT 
    ROUND(SUM(DEBT)/1000000, 2) AS total_debt
FROM international_debt; 

--Task5:

SELECT 
    COUNTRY_NAME,SUM(DEBT) AS total_debt
FROM international_debt
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1

--Task6:

SELECT 
    indicator_code AS debt_indicator,
    indicator_name,
    AVG(debt) AS average_debt
FROM international_debt
GROUP BY debt_indicator,indicator_name
ORDER BY 3 DESC
LIMIT 10

--Task7:

SELECT 
    country_name, 
    indicator_name
FROM international_debt
WHERE debt = (SELECT 
                 MAX(DEBT)
             FROM international_debt
             WHERE indicator_code = 'DT.AMT.DLXF.CD'
             )

--Task8:

SELECT indicator_code,COUNT(indicator_code) AS indicator_count
FROM international_debt
GROUP BY indicator_code
ORDER BY 2 DESC,1 DESC
LIMIT 20

--Task9:

SELECT country_name,MAX(DEBT) AS maximum_debt
FROM international_debt
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10