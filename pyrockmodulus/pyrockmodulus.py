import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import FuncFormatter
import time
import math

# Load UCS Strength Criterion py file
try:
    from . import ucs_descriptions
except ImportError:
    import ucs_descriptions
try:
    from . import formatting_codes
except ImportError:
    import formatting_codes

# START OF EXECUTION
abs_start = time.time()

'''
Default MATPLOTLIB Fonts
'''

# plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams["figure.figsize"] = [8,8]
matplotlib.rcParams['font.family'] = ['arial']
matplotlib.rcParams['font.size'] = 12

my_path = os.path.dirname(
    os.path.abspath(__file__))  # Figures out the absolute path for you in case your working directory moves around.


class modulus_ratio:
    """
    Based on the classification of Deere DU, Miller RP. Engineering Classification and Index Properties for Intact Rocks. Fort Belvoir, VA: Defense Technical Information Center; 1966.
    Data digitization courtesy of Rohatgi, Ankit. "WebPlotDigitizer." (2017).

    # ADVANCED: By assigning the *_rocktype_deere_miller_all* variable, more control over the clusters being plotted is gained.
    """
    ##TODO:
    # Allow to reset the xaxis and yaxis and house all the information
    # Allow to change the colors and have more control over what to plot in terms of sub-category of the rock type

    # Dictionary to hold Rock Category
    _rocktype_deere_miller_all = {"Diabase": ["Igneous", 'blue', 'ID'],
                                 "Granite": ["Igneous", 'black', "IG"],
                                 "Basalt": ["Igneous", 'red', "IF"],
                                 "Quartzite": ["Metamorphic", 'blue', ],
                                 "Gneiss": ["Metamorphic", 'red', "MG"],
                                 "Marble": ["Metamorphic", 'black', "MM"],
                                 "Schist_Flat": ["Metamorphic", 'darkgreen', "MSpp"],
                                 "Schist_Perp": ["Metamorphic", 'olive', "MSpl"],
                                 "Limestone": ["Sedimentary", 'black', "SL"],
                                 "Mudstone": ["Sedimentary", 'grey', "SSh"],
                                 "Sandstone": ["Sedimentary", 'red', "SS"],
                                 "Shale": ["Sedimentary", 'blue', 'SSh']}

    def load_data(self, df_deere_miller_data):
        """
        Load the file that holds the digital deere_miller cluster points. This information will be used to plot the deere-miller clusters based on the user requirements.

        :param df_deere_miller_data: file path to the location of the csv
        :type df_deere_miller_data: str

        :return: dictionary containing the type of rock and the points that form its cluster.
        :rtype: dict
        """

        global df_deere_miller

        # Load deere-miller digitized plots
        # Data digitization courtesy of Rohatgi, Ankit. "WebPlotDigitizer." (2017).
        df_deere_miller = pd.read_csv(os.path.join(my_path, 'Data', df_deere_miller_data), header=None)

        # Initialise the deere-miller as a dictionary
        db_deere_miller = {}

        for i in range(0, len(df_deere_miller.columns), 2):
            name = df_deere_miller.iloc[0,i]
            a = pd.Series(df_deere_miller.iloc[:,i].iloc[2:], dtype='float') # column of data frame
            b = pd.Series(df_deere_miller.iloc[:,i+1].iloc[2:], dtype='float')  # column of data frame (last_name)
            db_deere_miller[name] = [a, b]

        return db_deere_miller


    def plot_v_lines(self, vlines, ax):
        """
        Plot lines and annotate the UCS Strength Criteria adopted

        :param vlines: Locations of V Lines
        :type vlines: list[float]
        :param ax: Axis to plot
        :type ax: matplotlib

        :return:
        :rtype:
        """

        for i in vlines:
            plt.axvline(i, color='grey', linestyle='--', alpha=0.5)
        # Annotate the UCS Strength Criteria adopted
        for r_type_val in range(0, len(category_values) - 1):
            # Horizontal line at 80% of ymax
            plt.axhline(y=0.8 * self._ymax, color='grey', linestyle='--', alpha=0.5, zorder=-1)
            # Annotate only the values that lie in the range
            if category_values[r_type_val + 1] > self._xmin and category_values[r_type_val] <= self._xmax:
                if category_values[r_type_val + 1] > self._xmax:  # Condition that value > axis limit
                    ax.text(math.sqrt(self._xmax * category_values[r_type_val]), math.sqrt(self._ymax * (0.8 * self._ymax)),
                            category_names[r_type_val], ha='center', va='center', color='g', fontweight='bold')
                elif category_values[r_type_val] < self._xmin:  # Condition that value < axis limit
                    ax.text(math.sqrt(self._ymin * category_values[r_type_val + 1]), math.sqrt(self._ymax * (0.8 * self._ymax)),
                            category_names[r_type_val], ha='center', va='center', color='g', fontweight='bold')
                else:  # Values in between
                    ax.text(math.sqrt(category_values[r_type_val + 1] * category_values[r_type_val]),
                            math.sqrt(self._ymax * (0.8 * self._ymax)), category_names[r_type_val], ha='center', va='center', color='g',
                            fontweight='bold')


    def abline(self, slope, intercept, dr_state, multiplier=1, ratio='', ax=None):
        """
        Function to plot the slopped lines based on a slope and a y-intercept, basically mx+c. It is defined to form the Low/Avg/High MR ratio in the deere-miller classification plot.

        :param slope: the slope of the line
        :type slope: float
        :param intercept: the intercept of the lube
        :type intercept: float
        :param dr_state: draw state to move between the line drawing and the placement/writing of the text. Options [Line, Text]
        :type dr_state: str
        :param multiplier: in case of a need of a multiplier
        :type multiplier: int
        :param ratio: text associated with the MR modulus
        :type ratio: str
        :param ax: Matplotlib Axis
        :type ax: matplotlib

        :return:
        :rtype:
        """

        # Get axis limits
        axes = plt.gca()

        # Array the X as values from xlim
        x_vals = np.array(axes.get_xlim())

        # Get y values based on mx + c
        y_vals = intercept + (slope / multiplier) * x_vals

        # X-Location of text
        x_text_loc = 0.15
        txt_slope = np.rad2deg(np.arctan2(np.log(self._ymax-self._ymin), np.log(self._xmax-(self._xmin))))

        # Plot the mx+c line within axis limits
        # Y-value of text based on mx+c where X is predefined
        if dr_state == "line":
            ax.plot(x_vals, y_vals, color='grey', alpha=0.5, linestyle='--', zorder=-1)
            # Add the text to the sloped line
            ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc, '{:d}:1'.format(int(slope)), rotation=txt_slope, bbox=dict(facecolor='white', edgecolor="white"))
        # Add the text to category
        if dr_state == "text":
            ax.text(x_text_loc, intercept + (slope / multiplier) * x_text_loc,  ratio, rotation=txt_slope, alpha=0.5)


    def deere_miller_clusters(self, ax, df_of_clusters_deere_miller, r_type=None, plot_all_clusters_bool=False):
        """
        Load information needed to plot

        :param ax: Axis to plot on
        :type ax: matplotlib
        :param df_of_clusters_deere_miller: will plot defined cluster. Options Sedimentary, Igneous, Metamorphic.
        :type df_of_clusters_deere_miller: dict
        :param r_type: Define the rock type to be plotted. plot_all_clusters_bool MUST be false.
        :type r_type: str
        :param plot_all_clusters_bool: Plot all the clusters.
        :type plot_all_clusters_bool: bool

        :return:
        :rtype:
        """

        if not plot_all_clusters_bool and r_type=='':
            raise IndexError("If all clusters is disabled, the cluster to plot must be defined. df_of_clusters_deere_miller option should be Sedimentary, Igneous, Metamorphic")
        elif plot_all_clusters_bool and r_type != None:
            raise IndexError(
                "If all clusters is enabled. r_type should not be specified.")

        # Load dictionary of all the clusters and their default plotting information.
        # rocktype_deere_miller = rocktype_deere_miller_all
        if plot_all_clusters_bool:
            # Plot all k,v pair as Rock Type name (k) and cluster area (v)
            for k, v in self._rocktype_deere_miller_all.items():
                self.plot_clusters(k, v, ax, df_of_clusters_deere_miller)
        else:
            # Load k,v pair as Rock Type name (k) and cluster area (v)
            for k, v in self._rocktype_deere_miller_all.items():
                if v[0] == r_type:
                    self.plot_clusters(k ,v, ax, df_of_clusters_deere_miller)


    def plot_clusters(self, k, v, ax, df_of_clusters_deere_miller):
        """
        Plot the clusters

        :param k: key
        :type k: str
        :param v: value
        :type v: str
        :param ax: Axis to plot on
        :type ax: matplotlib
        :param df_of_clusters_deere_miller: dictionary containing the type of rock and the points that form its cluster.
        :type df_of_clusters_deere_miller: dict

        :return:
        :rtype:
        """

        # For Shale and Sandstone, plot open-ended clusters
        if k in ['Sandstone', 'Shale']:
            ax.plot(df_of_clusters_deere_miller[k][0], df_of_clusters_deere_miller[k][1], label=k, color=v[1], linewidth=1,
                    linestyle='--')
        # Schist has 2 areas
        elif k == 'Schist_Perp':
            ax.fill(df_of_clusters_deere_miller['Schist_Perp'][0], df_of_clusters_deere_miller['Schist_Perp'][1], fill=False,
                    label='Schist Perpendicular', color=v[1], linewidth=1, linestyle='--')
        elif k == 'Schist_Flat':
            ax.fill(df_of_clusters_deere_miller['Schist_Flat'][0], df_of_clusters_deere_miller['Schist_Flat'][1], fill=False,
                    label='Schist Parallel', color=v[1], linewidth=1, linestyle=':')
        else:
            cleanedListx = df_of_clusters_deere_miller[k][0][~np.isnan(df_of_clusters_deere_miller[k][0])]
            cleanedListy = df_of_clusters_deere_miller[k][1][~np.isnan(df_of_clusters_deere_miller[k][1])]
            ax.fill(cleanedListx, cleanedListy, fill=False, label=k, color=v[1], linewidth=1, closed=True)


    def format_axis(self, ax, state='', major_axis_vline = True):
        """
        Format log-log Axis

        :param ax: Axis to plot on
        :type ax: matplotlib
        :param state: state to enable to disable slopped lines
        :type state:
        :param major_axis_vline: Plot the major axis vlines
        :type major_axis_vline: bool
        :return:
        :rtype:
        """
        # Draw axis limits
        ax.set_xlim(self._xmin, self._xmax)
        ax.set_ylim(self._ymin, self._ymax)
        # Log-Log Scale
        ax.loglog()
        ax.grid(major_axis_vline, alpha=0.5, zorder=-1)
        # Format the Number to XX format for X and Y axis
        for axis in [ax.xaxis, ax.yaxis]:
            formatter = FuncFormatter(lambda ax_lab, _: '{:.16g}'.format(ax_lab))
            axis.set_major_formatter(formatter)

        if not state:
            # Draw SLopped line to presents different Areas
            self.abline(200 , 0, "line", 1000, '', ax)  # Slope of Strength Ratio Low:Average MPa to GPa
            self.abline(500 , 0, "line", 1000, '', ax)  # Slope of Strength Ratio Average:High MPa to GPa

            # Text to Classify the MR domains
            self.abline(800 , 0, "text", 1000, "High MR",ax)  # High MR
            self.abline(math.sqrt(200*500), 0, "text",1000, 'Average MR', ax)  # Average MR
            self.abline(100, 0, "text", 1000, 'Low MR',ax)  # Low MR


    def initial_processing(self, rock_type_to_plot=None, plot_all_clusters=False, ucs_class_type=None, ax=None):
        """
        Main function to plot the Modulus Ratio underlay

        :param rock_type_to_plot: Rock cluster type to plot.
        :type rock_type_to_plot: UCS Strength Criteria adopted. Options Sedimentary, Igneous, Metamorphic.
        :param ucs_class_type: UCS Strength Criteria adopted. Options 'ISRM\n1977', 'ISRMCAT\n1979', 'Bieniawski\n1974', 'Jennings\n1973', 'Broch & Franklin\n1972', 'Geological Society\n1970', 'Deere & Miller\n1966', 'Coates\n1964', 'Coates & Parsons\n1966', 'ISO 14689\n2017', 'Anon\n1977', 'Anon\n1979', 'Ramamurthy\n2004'
        :type ucs_class_type: str
        :param ax: Axis to plot on
        :type ax: matplotlib

        :return: Axis
        :rtype: Matplotlib Axis
        """

        # Load the data Deere Miller digitized plots
        df_of_clusters_deere_miller = self.load_data("Digitized_deere_miller.csv")

        # Indicate to user which curve is being plotted.
        if rock_type_to_plot:
            print("\tPlotting Modulus Ratio for %s Clusters" % formatting_codes.bold_text(rock_type_to_plot))
        else:
            print("\tPlotting Deere Miller for All Clusters")

        # Initialise Plotting Axis
        if ax is None:
            ax = plt.gca()
            self._xmin, self._xmax = 0.1, 500
            self._ymin, self._ymax = 0.01, 200

        self.deere_miller_clusters(ax, df_of_clusters_deere_miller, r_type=rock_type_to_plot, plot_all_clusters_bool=plot_all_clusters)

        # Load information for UCS Strength Criteria adopted
        global category_names, category_values
        if ucs_class_type:
            category_names, category_values = ucs_descriptions.ucs_strength_criteria(ucs_class_type)
            self.format_axis(ax, major_axis_vline=False)
            self.plot_v_lines(category_values, ax)
        else:
            self.format_axis(ax, major_axis_vline=True)

        return ax

class poisson_density():
    """
    Load Poisson Ratio and Density information
    """

    _poisson_density_range = [
        {'Rock Type': 'Andesite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.35, 'Min_D': 2.172, 'Max_D': 3.052},
        {'Rock Type': 'Basalt', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.35, 'Min_D': 0.736, 'Max_D': 3.124},
        {'Rock Type': 'Claystone', 'Group': 'Sedimentary', 'Min_P': 0.25, 'Max_P': 0.4, 'Min_D': 1.8, 'Max_D': 2.2},
        {'Rock Type': 'Conglomerate', 'Group': 'Sedimentary', 'Min_P': 0.1, 'Max_P': 0.4, 'Min_D': 2.47, 'Max_D': 2.76},
        {'Rock Type': 'Diabase/Dolerite', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.35, 'Min_D': 2.296, 'Max_D': 3.19},
        {'Rock Type': 'Diorite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.3, 'Min_D': 2.03, 'Max_D': 3.124},
        {'Rock Type': 'Dolomite', 'Group': 'Sedimentary', 'Min_P': 0.15, 'Max_P': 0.35, 'Min_D': 2.4, 'Max_D': 2.85},
        {'Rock Type': 'Gabbro', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.38, 'Min_D': 2.7, 'Max_D': 3.19},
        {'Rock Type': 'Gneiss', 'Group': 'Metamorphic', 'Min_P': 0.1, 'Max_P': 0.3, 'Min_D': 2.064, 'Max_D': 3.36},
        {'Rock Type': 'Granite', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 2.4, 'Max_D': 2.785},
        {'Rock Type': 'Granodiorite', 'Group': 'Igneous', 'Min_P': 0.15, 'Max_P': 0.25, 'Min_D': 2.63, 'Max_D': 2.74},
        {'Rock Type': 'Greywacke', 'Group': 'Sedimentary', 'Min_P': 0.08, 'Max_P': 0.23, 'Min_D': 2.41, 'Max_D': 2.77},
        {'Rock Type': 'Limestone', 'Group': 'Sedimentary', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 1.31, 'Max_D': 2.92},
        {'Rock Type': 'Marble', 'Group': 'Metamorphic', 'Min_P': 0.15, 'Max_P': 0.3, 'Min_D': 2.64, 'Max_D': 3.02},
        {'Rock Type': 'Marl', 'Group': 'Sedimentary', 'Min_P': 0.13, 'Max_P': 0.33, 'Min_D': 1.86, 'Max_D': 2.69},
        {'Rock Type': 'Norite', 'Group': 'Igneous', 'Min_P': 0.2, 'Max_P': 0.25, 'Min_D': 2.72, 'Max_D': 3.02},
        {'Rock Type': 'Quartzite', 'Group': 'Metamorphic', 'Min_P': 0.1, 'Max_P': 0.33, 'Min_D': 2.55, 'Max_D': 3.05},
        {'Rock Type': 'Rock Salt', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.3, 'Min_D': 2.1, 'Max_D': 2.9},
        {'Rock Type': 'Sandstone', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.4, 'Min_D': 1.44, 'Max_D': 2.8},
        {'Rock Type': 'Shale', 'Group': 'Sedimentary', 'Min_P': 0.05, 'Max_P': 0.32, 'Min_D': 1.6, 'Max_D': 2.92},
        {'Rock Type': 'Siltstone', 'Group': 'Sedimentary', 'Min_P': 0.13, 'Max_P': 0.35, 'Min_D': 1.11, 'Max_D': 2.87},
        {'Rock Type': 'Tuff', 'Group': 'Igneous', 'Min_P': 0.1, 'Max_P': 0.28, 'Min_D': 1.6, 'Max_D': 2.78}
    ]

    def initial_processing(self):
        """
        Load the variables and initialise the dataframe.

        :return: DataFrame containing the Min/Max Poisson Ratio and the Min/Max Density divided by Rock Name nad ROck Group. THe latter two impact the y-axis and the hbars and titles.
        :rtype: pandas.DataFrame

        """

        # Initialise DataFrame
        df = pd.DataFrame()
        # Read the data from the dictionary to a DataFrame
        df = df.from_dict(self._poisson_density_range)

        # Group the data based on the Major Rock Type
        df = df.sort_values(by=['Group', 'Rock Type'])

        # Get the span of the data which would be the difference between the min and max
        df['Max_D'] = df['Max_D'] - df['Min_D']
        df['Max_P'] = df['Max_P'] - df['Min_P']

        return df


    def plot_span_chart(self, df_to_plot, variable_span, variable_label, variable_units, ax=None):
        """
        Plot a chart divided by the rock type and rock group.

        :param df_to_plot: Panda Dataframe to plot
        :type df_to_plot: pandas.DataFrame
        :param variable_span: Span (i.e., min and max values) passed as a list. Must be the Column Header name in the DataFrame!
        :type variable_span: list[str, str]
        :param variable_label: Variable Name. X axis label
        :type variable_label: str
        :param variable_units: Variable Units. X axis label unit
        :type variable_units: str
        :param ax: Matplotlib Axis to plot On
        :type ax: Matplolib

        :return: Matplotlib AxesSubplots
        :rtype: Matplotlib Axis
        """

        # Initialise Plotting Axis
        if ax is None:
            ax = plt.gca()

        # Divide the data into groups
        dfx = df_to_plot.groupby(['Group'])

        # Get the total number of groups
        size = dfx.size()

        # Get data for the Span Chart
        # X is the Rock Name and Y is the Parameter to plot
        # Change the grey to the required bar color
        df_to_plot.plot.barh(x='Rock Type', y=variable_span, stacked=True, color=['white', 'grey'], alpha=0.5, ax=ax)

        # If groups are defined, Assign initial locations
        hline_loc = 0
        hline_loc_old = 0
        counter = 1
        for k, v in dfx:
            hline_loc += len(v)  # New location is after the first group
            if counter != len(size):
                plt.axhline(hline_loc - 0.5, ls='--', color='black', alpha=0.5)  # Plot Division Line
            # Annotate text in the middle of the group with a white background
            plt.text(0.025 * plt.gca().get_xlim()[1], (hline_loc_old + hline_loc - 1) / 2, k, rotation=90,
                     color='green', fontweight='bold', va='center', bbox=dict(boxstyle="square",
                                                                              ec=(1., 1., 1.),
                                                                              fc=(1., 1., 1.),
                                                                              ))
            hline_loc_old = hline_loc  # Update line location
            # Condition to skip over and not draw the last line
            counter += 1

        # Cosmetics to the plotted curve
        # Disable any y-label information as this is determined by the DataFrame being plotted
        plt.ylabel('')
        # Plot the xlabel information based on the variables label and units passed.
        if ' ' not in variable_units:
            plt.xlabel("%s, %s" % (variable_label, variable_units))
        else:
            plt.xlabel("%s, %s (%s)" % (variable_label, variable_units.split(' ')[0], variable_units.split(' ')[1]))
        plt.legend().set_visible(False)

        return ax

'''
MAIN MODULE
- Returns total time and Error on user termination.
'''

if __name__ == "__main__":
    try:
        # Names of files are defined in initial_processing - load_data module
        # INPUT x_para, y_para, x_para name, y_para name,  UCS Strength Criteria adopted, "Rock"//"Replica"
        plx = modulus_ratio().initial_processing(plot_all_clusters=False, rock_type_to_plot='Sedimentary', ucs_class_type="ISRMCAT\n1979")
        plx.scatter(10, 10, label="DataPoint")
        # Cosmetics to the figure and layouts
        plt.xlabel("UCS")
        plt.ylabel("Emod")
        plx.legend()
        plt.show()
        print("\nTotal Execution time: \033[1m%s\033[0m\n" % calc_timer_values(time.time() - abs_start))
    except KeyboardInterrupt:
        exit("TERMINATED BY USER")