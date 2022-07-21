#!/usr/bin/env python
# coding: utf-8

# ## 1. Inspecting the data
# <p><img src="https://assets.datacamp.com/production/project_1416/img/schoolbus.jpg" alt="New York City schoolbus" height="300px" width="300px"></p>
# <p>Photo by <a href="https://unsplash.com/@jannis_lucas">Jannis Lucas</a> on <a href="https://unsplash.com">Unsplash</a>.
# <br></p>
# <p>Every year, American high school students take SATs, which are standardized tests intended to measure literacy, numeracy, and writing skills. There are three sections - reading, math, and writing, each with a maximum score of 800 points. These tests are extremely important for students and colleges, as they play a pivotal role in the admissions process.</p>
# <p>Analyzing the performance of schools is important for a variety of stakeholders, including policy and education professionals, researchers, government, and even parents considering which school their children should attend. </p>
# <p>In this notebook, we will take a look at data on SATs across public schools in New York City. Our database contains a single table:</p>
# <h1 id="schools"><code>schools</code></h1>
# <table>
# <thead>
# <tr>
# <th>column</th>
# <th>type</th>
# <th>description</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td><code>school_name</code></td>
# <td><code>varchar</code></td>
# <td>Name of school</td>
# </tr>
# <tr>
# <td><code>borough</code></td>
# <td><code>varchar</code></td>
# <td>Borough that the school is located in</td>
# </tr>
# <tr>
# <td><code>building_code</code></td>
# <td><code>varchar</code></td>
# <td>Code for the building</td>
# </tr>
# <tr>
# <td><code>average_math</code></td>
# <td><code>int</code></td>
# <td>Average math score for SATs</td>
# </tr>
# <tr>
# <td><code>average_reading</code></td>
# <td><code>int</code></td>
# <td>Average reading score for SATs</td>
# </tr>
# <tr>
# <td><code>average_writing</code></td>
# <td><code>int</code></td>
# <td>Average writing score for SATs</td>
# </tr>
# <tr>
# <td><code>percent_tested</code></td>
# <td><code>numeric</code></td>
# <td>Percentage of students completing SATs</td>
# </tr>
# </tbody>
# </table>
# <p>Let's familiarize ourselves with the data by taking a looking at the first few schools!</p>

# In[94]:


get_ipython().run_cell_magic('sql', '', 'postgresql:///schools\n    \n-- Select all columns from the database\n-- Display only the first ten rows\nSELECT * \nFROM SCHOOLS\nLIMIT 10')


# In[95]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\n\ndef test_task1_output_type():\n    assert str(type(last_output)) == "<class \'sql.run.ResultSet\'>", \\\n    "Please ensure an SQL ResultSet is the output of the code cell." \n\nresults = last_output.DataFrame()\n\ndef test_task1_results():\n    assert results.shape == (10, 7), \\\n    "The results should have fourteen columns and ten rows."\n    assert set(results.columns) == set([\'school_name\', \'borough\', \'building_code\', \'average_math\', \'average_reading\', \'average_writing\', \'percent_tested\']), \\\n    \'The results should include all columns from the database, without using an alias.\'\n    assert last_output.DataFrame().loc[0, \'building_code\'] == "M022", \\\n    "The building code for the first school should be M022."')


# ## 2. Finding missing values
# <p>It looks like the first school in our database had no data in the <code>percent_tested</code> column! </p>
# <p>Let's identify how many schools have missing data for this column, indicating schools that did not report the percentage of students tested. </p>
# <p>To understand whether this missing data problem is widespread in New York, we will also calculate the total number of schools in the database.</p>

# In[96]:


get_ipython().run_cell_magic('sql', '', '\n-- Count rows with percent_tested missing and total number of schools\nSELECT COUNT(SCHOOL_NAME)-COUNT(PERCENT_TESTED) AS num_tested_missing , \n        COUNT(SCHOOL_NAME) AS num_schools\nFROM SCHOOLS ')


# In[97]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task2_columns():\n    assert last_output_df.shape == (1, 2), \\\n    "Did you correctly select the data? Expected the result to contain one row and two columns?"\n    assert set(last_output_df.columns) == set(["num_tested_missing", "num_schools"]), \\\n    "Did you use the alias `num_tested_missing` and also select the `num_schools` column?"\n\ndef test_task2_output():\n    assert last_output_df.iloc[0, 0] == 20, \\\n    """Did you correctly calculate `"num_tested_missing"?"""\n    assert last_output_df.iloc[0, 1] == 375, \\\n    """Did you correctly calculate the total number of rows in the database?"""  ')


# ## 3. Schools by building code
# <p>There are 20 schools with missing data for <code>percent_tested</code>, which only makes up 5% of all rows in the database.</p>
# <p>Now let's turn our attention to how many schools there are. When we displayed the first ten rows of the database, several had the same value in the <code>building_code</code> column, suggesting there are multiple schools based in the same location. Let's find out how many unique school locations exist in our database. </p>

# In[98]:


get_ipython().run_cell_magic('sql', '', '\n-- Count the number of unique building_code values\nSELECT COUNT(DISTINCT BUILDING_CODE) AS num_school_buildings\nFROM SCHOOLS')


# In[99]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task3_column_name():\n    assert last_output_df.columns.tolist() == ["num_school_buildings"], \\\n    "Did you use the correct alias for the number of unique school buildings?"\n\ndef test_task3_value():\n    assert last_output_df.values.tolist() == [[233]], \\\n    "Did you use the correct method to calculate how many unique school buildings are in the database? Expected a different value."')


# ## 4. Best schools for math
# <p>Out of 375 schools, only 233 (62%) have a unique <code>building_code</code>! </p>
# <p>Now let's start our analysis of school performance. As each school reports individually, we will treat them this way rather than grouping them by <code>building_code</code>. </p>
# <p>First, let's find all schools with an average math score of at least 80% (out of 800). </p>

# In[100]:


get_ipython().run_cell_magic('sql', '', '\n-- Select school and average_math\n-- Filter for average_math 640 or higher\n-- Display from largest to smallest average_math\nSELECT SCHOOL_NAME,AVERAGE_MATH\nFROM SCHOOLS\nWHERE AVERAGE_MATH >= 640\nORDER BY AVERAGE_MATH DESC')


# In[101]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task4_columns():\n    assert set(last_output_df.columns) == set(["school_name", "average_math"]), \\\n    "Did you select the correct columns?"\n\ndef test_task4_filter():\n    assert last_output_df["average_math"].min() >= 640, \\\n    """Did you correctly filter for "average_math" scores more than or equal to 640?"""\n    assert last_output_df.shape == (10, 2), \\\n    """The output has the wrong number of results, did you correctly filter the "average_math" column?"""\n\ndef test_task4_values():\n    assert last_output_df.iloc[0,0] == "Stuyvesant High School", \\\n    """Did you run the correct query? Expected the first school to be "Stuyvesant High School"."""\n    assert last_output_df.iloc[0,1] == 754.0, \\\n    """Did you correctly sort the values by "average_math" in descending order? Expected a different range of results."""')


# ## 5. Lowest reading score
# <p>Wow, there are only ten public schools in New York City with an average math score of at least 640!</p>
# <p>Now let's look at the other end of the spectrum and find the single lowest score for reading. We will only select the score, not the school, to avoid naming and shaming!</p>

# In[102]:


get_ipython().run_cell_magic('sql', '', '\n-- Find lowest average_reading\nSELECT MIN(AVERAGE_READING) AS lowest_reading\nFROM SCHOOLS')


# In[103]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task5_value():  \n    assert last_output_df["lowest_reading"].values.tolist() == [302.0], \\\n    """Did you select the minimum value for the "average_reading" column?"""\n\ndef test_task5_alias():\n    assert last_output_df.columns.tolist() == ["lowest_reading"], \\\n    """Did you use the correct alias? Expected "lowest_reading"."""')


# ## 6. Best writing school
# <p>The lowest average score for reading across schools in New York City is less than 40% of the total available points! </p>
# <p>Now let's find the school with the highest average writing score.</p>

# In[104]:


get_ipython().run_cell_magic('sql', '', '\n-- Find the top score for average_writing\n-- Group the results by school\n-- Sort by max_writing in descending order\n-- Reduce output to one school\nSELECT SCHOOL_NAME,MAX(AVERAGE_WRITING) AS max_writing\nFROM SCHOOLS\nGROUP BY SCHOOL_NAME\nORDER BY MAX_WRITING DESC\nLIMIT 1')


# In[105]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task6_columns():\n    assert set(last_output_df.columns) == set(["school_name", "max_writing"]), \\\n    """Did you select "average_writing" and use an alias?"""\n    \ndef test_task6_shape():\n    assert last_output_df.shape[0] == 1, \\\n    "Did you select the correct number of values? Expected one row."\n\ndef test_task6_values():\n    assert last_output_df.values.tolist() == [[\'Stuyvesant High School\', 693.0]], \\\n    """Did you select the maximum value for "average_writing"? Expected a different value."""  ')


# ## 7. Top 10 schools
# <p>An average writing score of 693 is pretty impressive! </p>
# <p>This top writing score was at the same school that got the top math score, Stuyvesant High School. Stuyvesant is widely known as a perennial top school in New York. </p>
# <p>What other schools are also excellent across the board? Let's look at scores across reading, writing, and math to find out.</p>

# In[106]:


get_ipython().run_cell_magic('sql', '', '\n-- Calculate average_sat\n-- Group by school_name\n-- Sort by average_sat in descending order\n-- Display the top ten results\nSELECT SCHOOL_NAME,(AVERAGE_MATH+AVERAGE_READING+AVERAGE_WRITING) AS average_sat\nFROM SCHOOLS\nGROUP BY SCHOOL_NAME\nORDER BY AVERAGE_SAT DESC\nLIMIT 10')


# In[107]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task7_columns():\n    assert set(last_output_df.columns) == set(["school_name", "average_sat"]), \\\n    """Did you select the correct columns and use an alias for the sum of the three sat score columns?"""\n    \ndef test_task7_shape():\n    assert last_output_df.shape[0] == 10, \\\n    "Did you limit the number of results to ten?"\n    assert last_output_df.shape[1] == 2, \\\n    """Expected your query to return two columns: "school_name" and "average_sat"."""\n\ndef test_task7_values():\n    assert last_output_df.iloc[0].values.tolist() == [\'Stuyvesant High School\', 2144], \\\n    """Did you correctly define your query? Expected different values for the first school."""\n    assert last_output_df["average_sat"].min() == 1889, \\\n    """Did you correctly filter the results? Expected a different lowest score for "average_sat"."""  \n    assert last_output_df["average_sat"].max() == 2144, \\\n    """Did you correctly calculate the "average_sat" column? Expected a different top score."""')


# ## 8. Ranking boroughs
# <p>There are four schools with average SAT scores of over 2000! Now let's analyze performance by New York City borough. </p>
# <p>We will build a query that calculates the number of schools and the average SAT score per borough!</p>

# In[108]:


get_ipython().run_cell_magic('sql', '', '\n-- Select borough and a count of all schools, aliased as num_schools\n-- Calculate the sum of average_math, average_reading, and average_writing, divided by a count of all schools, aliased as average_borough_sat\n-- Organize results by borough\n-- Display by average_borough_sat in descending order\nSELECT BOROUGH,COUNT(SCHOOL_NAME) AS num_schools,\n     (SUM(AVERAGE_MATH)+SUM(AVERAGE_READING)+SUM(AVERAGE_WRITING))/COUNT(SCHOOL_NAME) AS average_borough_sat\nFROM SCHOOLS\nGROUP BY BOROUGH\nORDER BY average_borough_sat DESC')


# In[109]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task8_columns():\n    assert set(last_output_df.columns) == set([\'borough\', \'num_schools\', \'average_borough_sat\']), \\\n    """Did you select the correct columns and use aliases for the number of schools and average sat scores?"""\n\ndef test_task8_shape():\n    assert last_output_df.shape[0] == 5, \\\n    "Did you group by the correct column? Expected five rows to be returned: one for each borough."\n    assert last_output_df.shape[1] == 3, \\\n    """Expected your query to return three columns: "borough", "num_schools", and "average_borough_sat"."""\n\ndef test_task8_values():\n    # Each assert statement checks values per row \n    assert last_output_df.iloc[0].values.tolist() == [\'Staten Island\', 10, 1439], \\\n    """Did you correctly define your query? Expected different values for Staten Island."""\n    assert last_output_df.iloc[1].values.tolist() == [\'Queens\', 69, 1345], \\\n    """Did you correctly define your query? Expected different values for Queens."""\n    assert last_output_df.iloc[2].values.tolist() == [\'Manhattan\', 89, 1340], \\\n    """Did you correctly define your query? Expected different values for Manhattan."""\n    assert last_output_df.iloc[3].values.tolist() == [\'Brooklyn\', 109, 1230], \\\n    """Did you correctly define your query? Expected different values for Brooklyn."""\n    assert last_output_df.iloc[4].values.tolist() == [\'Bronx\', 98, 1202], \\\n    """Did you correctly define your query? Expected different values for the Bronx."""\n    # Check lowest average_reading score is in the last row\n    assert last_output_df.iloc[-1, 0] == \'Bronx\', \\\n    """Did you sort the results by "average_sat" in descending order?"""')


# ## 9. Brooklyn numbers
# <p>It appears that schools in Staten Island, on average, produce higher scores across all three categories. However, there are only 10 schools in Staten Island, compared to an average of 91 schools in the other four boroughs!</p>
# <p>For our final query of the database, let's focus on Brooklyn, which has 109 schools. We wish to find the top five schools for math performance.</p>

# In[110]:


get_ipython().run_cell_magic('sql', '', "\n-- Select school and average_math\n-- Filter for schools in Brooklyn\n-- Aggregate on school_name\n-- Display results from highest average_math and restrict output to five rows\nSELECT SCHOOL_NAME,AVERAGE_MATH\nFROM SCHOOLS\nWHERE BOROUGH = 'Brooklyn'\nORDER BY 2 DESC\nLIMIT 5")


# In[111]:


get_ipython().run_cell_magic('nose', '', 'last_output = _\nlast_output_df = last_output.DataFrame()\n\ndef test_task9_columns():\n    assert last_output_df.columns.tolist() == [\'school_name\', \'average_math\'], \\\n    """Did you select the correct columns? Expected "school_name" and "average_math"."""\n    \ndef test_task9_shape():\n    assert last_output_df.shape[0] == 5, \\\n    "Did you limit the output to 5 rows?"\n    assert last_output_df.shape[1] == 2, \\\n    "Did you select the correct number of columns? Expected two."\n    \ndef test_task9_school_names():\n    assert last_output_df["school_name"].tolist() == [\'Brooklyn Technical High School\', \'Brooklyn Latin School\', \'Leon M. Goldstein High School for the Sciences\', \'Millennium Brooklyn High School\', \'Midwood High School\'], \\\n    "Did you correctly filter by borough? Expected a different list of school names."\n    \ndef test_task9_values():\n    assert last_output_df["average_math"].max() == 682, \\\n    """Did you select the correct values? Expected a maximum value of 682.0 for "average_math"."""    \n    assert last_output_df["average_math"].min() == 550, \\\n    """Did you select the correct values? Expected a minimum value of 550.0 for "average_math"."""\n    assert last_output_df["average_math"].values.tolist() == [682, 625, 563, 553, 550], \\\n    """Did you sort by "average_math" in descending order? Expected different values."""')

