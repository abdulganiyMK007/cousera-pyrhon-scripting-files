"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(
            csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo   - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    country_codes_data = read_csv_as_nested_dict(
        codeinfo["codefile"], codeinfo["plot_codes"], codeinfo["separator"], codeinfo["quote"])

    plot_to_wb_codes = {}
    for data in country_codes_data.values():
        plot_code = data[codeinfo["plot_codes"]]
        wb_code = data[codeinfo["data_codes"]]
        plot_to_wb_codes[plot_code] = wb_code
    return plot_to_wb_codes


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    plot_to_wb_codes = build_country_code_converter(codeinfo)
    found_countries_dict = {}
    unfound_countries_set = set()

    for gdp_code in gdp_countries:
        for plot_code in plot_countries:
            if plot_to_wb_codes[plot_code.upper()] == gdp_code:
                found_countries_dict[plot_code] = plot_to_wb_codes[plot_code.upper(
                )]

    for plot_code in plot_countries:
        if found_countries_dict.get(plot_code) is None:
            unfound_countries_set.add(plot_code)

    return found_countries_dict, unfound_countries_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_countries = read_csv_as_nested_dict(
        gdpinfo["gdpfile"], gdpinfo["country_code"], gdpinfo["separator"], gdpinfo["quote"])

    reconciled_names = reconcile_countries_by_code(codeinfo,
        plot_countries, gdp_countries)

    found_countries_dict = reconciled_names[0]
    unfound_country_codes_set = reconciled_names[1]

    found_empty_data_countries_code = set()
    found_countries_data_dict = {}
    
    for plot_code, wb_code in found_countries_dict.items():
        gdp_in_year = gdp_countries[wb_code].get(year)
        if gdp_in_year in ('0', ""):
            found_empty_data_countries_code.add(plot_code)
        else:
            found_countries_data_dict[plot_code] = math.log(float(gdp_in_year), 10)

    return found_countries_data_dict, unfound_country_codes_set, found_empty_data_countries_code


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    data_dict = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = 'World GDP in the year ' + year
    worldmap_chart.add(f'In {year}', data_dict[0])
    worldmap_chart.add('Missing from World data', data_dict[1])
    worldmap_chart.add('No GDP data', data_dict[2])
    # worldmap_chart.render_in_browser()
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries,
                     "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries,
                     "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries,
                     "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries,
                     "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
