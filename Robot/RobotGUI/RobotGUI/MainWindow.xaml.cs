using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace RobotGUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void quitEvent(object sender, RoutedEventArgs e)
        {
            //Closes the GUI on quit button press
            Application.Current.Shutdown();
        }

        private void voiceCommandEvent(object sender, RoutedEventArgs e)
        {
            //Executes the script for the robot to recognise voice commands
            batchExecute("D:\\Erik_Thomas\\Robot\\robot_compiled\\voice_commands.bat");
        }

        private void gestureRecognitionEvent(object sender, RoutedEventArgs e)
        {
            //Executes the script for gesture recognition
            batchExecute("D:\\Erik_Thomas\\Robot\\robot_compiled\\mirror_movement.bat");
        }

        private static void batchExecute(string command)
        {
            //Creates a new command line process, the string 'command' takes a file path and any other relevant parts of the command
            var processInfo = new ProcessStartInfo("cmd.exe", "/c " + command);
            //The settings for the command line process are initialised
            processInfo.CreateNoWindow = false;
            processInfo.UseShellExecute = true;
            processInfo.RedirectStandardError = false;
            processInfo.RedirectStandardOutput = false;
            //A process is used to store the specific command line process
            var process = Process.Start(processInfo);

            process.WaitForExit();

            Console.WriteLine("ExitCode: {0}", process.ExitCode);
            process.Close();
        }
    }
}
