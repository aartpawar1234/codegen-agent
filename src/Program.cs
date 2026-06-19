using System;
using TodoApp.Models;
using TodoApp.Services;

namespace TodoApp
{
    /// <summary>
    /// Entry point of the to-do list application.
    /// </summary>
    public class Program
    {
        private static readonly TodoService _todoService = new TodoService();

        /// <summary>
        /// Main entry point of the application.
        /// </summary>
        public static void Main(string[] args)
        {
            Console.WriteLine("Welcome to the To-Do List Application!");
            Console.WriteLine("--------------------------------------");

            while (true)
            {
                Console.WriteLine("\nChoose an option:");
                Console.WriteLine("1. Add a new to-do item");
                Console.WriteLine("2. List all to-do items");
                Console.WriteLine("3. Update a to-do item");
                Console.WriteLine("4. Delete a to-do item");
                Console.WriteLine("5. Exit");
                Console.Write("Enter your choice (1-5): ");

                var choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        AddTodoItem();
                        break;
                    case "2":
                        ListTodoItems();
                        break;
                    case "3":
                        UpdateTodoItem();
                        break;
                    case "4":
                        DeleteTodoItem();
                        break;
                    case "5":
                        Console.WriteLine("Exiting the application. Goodbye!");
                        return;
                    default:
                        Console.WriteLine("Invalid choice. Please try again.");
                        break;
                }
            }
        }

        private static void AddTodoItem()
        {
            Console.Write("Enter title: ");
            var title = Console.ReadLine();

            Console.Write("Enter description: ");
            var description = Console.ReadLine();

            try
            {
                var item = _todoService.Add(title, description);
                Console.WriteLine($"To-do item added successfully! ID: {item.Id}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private static void ListTodoItems()
        {
            var items = _todoService.GetAll();

            if (items.Count == 0)
            {
                Console.WriteLine("No to-do items found.");
                return;
            }

            Console.WriteLine("\nTo-Do Items:");
            Console.WriteLine("--------------------------------------");
            foreach (var item in items)
            {
                Console.WriteLine($"ID: {item.Id}");
                Console.WriteLine($"Title: {item.Title}");
                Console.WriteLine($"Description: {item.Description}");
                Console.WriteLine($"Completed: {(item.IsCompleted ? "Yes" : "No")}");
                Console.WriteLine($"Created At: {item.CreatedAt:yyyy-MM-dd HH:mm:ss}");
                Console.WriteLine("--------------------------------------");
            }
        }

        private static void UpdateTodoItem()
        {
            Console.Write("Enter the ID of the item to update: ");
            if (!int.TryParse(Console.ReadLine(), out var id))
            {
                Console.WriteLine("Invalid ID. Please enter a valid number.");
                return;
            }

            var item = _todoService.GetById(id);
            if (item == null)
            {
                Console.WriteLine("Item not found.");
                return;
            }

            Console.WriteLine($"Current Title: {item.Title}");
            Console.Write("Enter new title (leave blank to keep current): ");
            var title = Console.ReadLine();

            Console.WriteLine($"Current Description: {item.Description}");
            Console.Write("Enter new description (leave blank to keep current): ");
            var description = Console.ReadLine();

            Console.WriteLine($"Current Completed Status: {(item.IsCompleted ? "Yes" : "No")}");
            Console.Write("Mark as completed? (y/n, leave blank to keep current): ");
            var completedInput = Console.ReadLine();
            var isCompleted = completedInput?.Trim().ToLower() == "y" || item.IsCompleted;

            try
            {
                var success = _todoService.Update(id, string.IsNullOrEmpty(title) ? item.Title : title,
                    string.IsNullOrEmpty(description) ? item.Description : description, isCompleted);

                if (success)
                {
                    Console.WriteLine("To-do item updated successfully!");
                }
                else
                {
                    Console.WriteLine("Failed to update item.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private static void DeleteTodoItem()
        {
            Console.Write("Enter the ID of the item to delete: ");
            if (!int.TryParse(Console.ReadLine(), out var id))
            {
                Console.WriteLine("Invalid ID. Please enter a valid number.");
                return;
            }

            try
            {
                var success = _todoService.Delete(id);
                if (success)
                {
                    Console.WriteLine("To-do item deleted successfully!");
                }
                else
                {
                    Console.WriteLine("Item not found.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}
