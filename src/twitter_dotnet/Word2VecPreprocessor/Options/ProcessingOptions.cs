using System;
using System.IO;
using CommandLine;
using JetBrains.Annotations;

namespace Word2VecPreprocessor.Options
{
    /// <summary>
    /// A model that holds the user options when invoking the program
    /// </summary>
    public sealed class ProcessingOptions
    {
        /// <summary>
        /// Gets or sets the source folder to use to read the tweets
        /// </summary>
        [Option('s', "source", HelpText = "The source folder to use to read the saved tweets.", Required = true)]
        public string SourceFolder { get; set; }

        /// <summary>
        /// Gets or sets the path of the file that contains the user ids for the different communities
        /// </summary>
        [Option('c', "communities", HelpText = "The file that holds the list of ids for users in different communities.", Required = true)]
        public string CommunitiesFile { get; set; }

        /// <summary>
        /// Gets or sets the destination folder to use to store the results
        /// </summary>
        [Option('d', "destination", HelpText = "The destination folder to use to store the results.", Required = true)]
        public string DestinationFolder { get; set; }

        /// <summary>
        /// Gets or sets the number of dictionary words to use
        /// </summary>
        [Option('w', "words", HelpText = "The number of dictionary words to save.", Required = true)]
        public int Words { get; set; }

        /// <summary>
        /// Executes a preliminary validation of the current instance
        /// </summary>
        [AssertionMethod]
        public void Validate()
        {
            // Source folder path
            if (string.IsNullOrEmpty(SourceFolder)) throw new ArgumentException("The source folder path can't be empty");
            if (!Directory.Exists(SourceFolder)) throw new ArgumentException("The source folder doesn't exist");

            // Communities file
            if (string.IsNullOrEmpty(CommunitiesFile)) throw new ArgumentException("The communities file path can't be empty");
            if (!File.Exists(CommunitiesFile)) throw new ArgumentException("The communities file doesn't exist");

            // Destination directory
            if (string.IsNullOrEmpty(DestinationFolder)) throw new ArgumentException("The destination folder path can't be empty");
            if (!Directory.Exists(DestinationFolder)) throw new ArgumentException("The destination directory doesn't exist");

            // Other parameters
            if (Words <= 0) throw new ArgumentException("The number of words must be a positive number");
        }
    }
}