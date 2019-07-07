using System;
using CommandLine;
using Word2VecPreprocessor.Core;
using Word2VecPreprocessor.Options;

namespace Word2VecPreprocessor
{
    public sealed class Program
    {
        public static void Main(string[] args)
        {
            new Parser()
                .ParseArguments<ProcessingOptions>(args)
                .WithParsed(ProcessingEngine.Process)
                .WithNotParsed(errors =>
                {
                    foreach (var error in errors)
                        Console.WriteLine(error.ToString());
                });

            Console.ReadKey();
        }
    }
}
