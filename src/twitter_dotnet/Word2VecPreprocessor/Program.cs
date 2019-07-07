﻿using System;
using System.Threading;
using CommandLine;
using Word2VecPreprocessor.Core;
using Word2VecPreprocessor.Options;

namespace Word2VecPreprocessor
{
    public sealed class Program
    {
        public static void Main(string[] args)
        {
            new Parser(with => with.AutoHelp = true)
                .ParseArguments<ProcessingOptions>(args)
                .WithParsed(options =>
                {
                    options.Validate();
                    ProcessingEngine.Process(options);
                })
                .WithNotParsed(errors =>
                {
                    foreach (var error in errors)
                        Console.WriteLine(error.ToString());
                });

            Console.Beep(); Thread.Sleep(150); Console.Beep(); // Two high-pitched beeps to indicate success
            Console.ReadKey();
        }
    }
}
