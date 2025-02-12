import os
import sys
from typing import List


class MinHeap:
    def __init__(self):
    # Initialize an empty list to represent the min-heap
        self.minHeap = []
    def _str_(self):
     # Return a string representation of the min-heap
        return ", ".join(str(item) for item in self.minHeap)
    def is_empty(self):
    # Check if the min-heap is empty
        return len(self.minHeap) == 0
    def get_all_elements(self):
     # Return all elements in the min-heap
        return self.minHeap
    def insert(self, node):
     # Insert a node into the min-heap and maintain the heap property
        self.minHeap.append(node)
        currentIndex = len(self.minHeap) - 1
        while currentIndex > 0:
            parentIndex = (currentIndex - 1) // 2
            parent = self.minHeap[parentIndex]
             # Compare the priority of the current node with its parent
            if node.compare(parent):
                self.minHeap[currentIndex], self.minHeap[parentIndex] = self.minHeap[parentIndex], node
                currentIndex = parentIndex
            else:
                break
    def get_min(self):
     # Return the minimum element in the min-heap
        if len(self.minHeap) == 0:
            return None
        return self.minHeap[0]
    def remove_min(self):
     # Remove and return the minimum element from the min-heap
        if len(self.minHeap) == 0:
            return None
        minNode = self.get_min()
        lastNode = self.minHeap.pop()
        if len(self.minHeap) != 0:
            self.minHeap[0] = lastNode
            currentIndex = 0
            while True:
                leftIndex = 2 * currentIndex + 1
                rightIndex = 2 * currentIndex + 2
                if leftIndex >= len(self.minHeap):
                    break
                minChildIndex = leftIndex
                if rightIndex < len(self.minHeap):
                    left = self.minHeap[leftIndex]
                    right = self.minHeap[rightIndex]
                    if left.compare(right):
                        minChildIndex = rightIndex
                minChild = self.minHeap[minChildIndex]
                if lastNode.compare(minChild):
                    self.minHeap[currentIndex], self.minHeap[minChildIndex] = minChild, lastNode
                    currentIndex = minChildIndex
                else:
                    break
        return minNode
    def delete(self, node):
     # Delete a specific node from the min-heap
        if len(self.minHeap) == 0:
            return
        try:
            index = self.minHeap.index(node)
        except ValueError:
            return
        lastNode = self.minHeap.pop()
        if index != len(self.minHeap):
            self.minHeap[index] = lastNode
            currentIndex = index
            while True:
                leftIndex = 2 * currentIndex + 1
                rightIndex = 2 * currentIndex + 2
                if leftIndex >= len(self.minHeap):
                    break
                minChildIdx = leftIndex
                if rightIndex < len(self.minHeap):
                    left = self.minHeap[leftIndex]
                    right = self.minHeap[rightIndex]
                    if left.compare(right):
                        minChildIdx = rightIndex
                minChild = self.minHeap[minChildIdx]
                if lastNode.compare(minChild):
                    self.minHeap[currentIndex], self.minHeap[minChildIdx] = minChild, lastNode
                    currentIndex = minChildIdx
                else:
                    break
                parentIndex = (currentIndex - 1) // 2
                if currentIndex > 0 and lastNode.compare(self.minHeap[parentIndex]):
                    while currentIndex > 0:
                        parentIndex = (currentIndex - 1) // 2
                        parent = self.minHeap[parentIndex]
                        if lastNode.compare(parent):
                            self.minHeap[currentIndex], self.minHeap[parentIndex] = parent, lastNode
                            currentIndex = parentIndex
                        else:
                            break
class Patron:
#Represents a library patron with an ID and priority level.
    def __init__(self, patronId, patronPriority) -> None:
    #Initializes the patron with the provided ID and priority.#
        self.patronId = patronId
        self.patronPriority = patronPriority
    def compare(self, other):
    #Compares the priority levels of two patrons.#
        return self.patronPriority < other.patronPriority
    def _str_(self):
    #Returns a string representation of the patron.#
        return f"PatronID: {self.patronId}, Priority: {self.patronPriority}"
    def _gt_(self, other):
    #Checks if the current patron has a higher priority than another.#
        return self.patronPriority > other.patronPriority
# Node creation
class Book():
 #Represents a library book with details and reservation management.#
   
     #Initializes the book with the provided details.#
    def __init__(self, bookId, bookName, authorName, availabilityStatus):
        self.bookId = bookId
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = None
        self.reservationHeap = MinHeap()
        self.parent = None
        self.left = None
        self.right = None
        self._color = 1
        self.transformations = -1
        self.flipCount=0
    @property
    def color(self):
     #Returns the current color of the node.#
        return self._color
    @color.setter
    def color(self, value):
     #Updates the color of the node.#
        self.transformations += 1
        self._color = value
    def _str_(self) -> str:
     #Returns a detailed string representation of the book.#
        reservations_str = ", ".join([str(patron.patronId) for patron in self.reservationHeap.get_all_elements()])
        book_info = (
            f"BookId = {self.bookId}\n"
            f"Title = {self.bookName}\n"
            f"Author = {self.authorName}\n"
            f"Availability = {self.availabilityStatus}\n"
            f"BorrowedBy = {self.borrowedBy}\n"
            f"Reservations = [{reservations_str}]"
        )
        return book_info
    def __insert_into_reservation(self, patronId, patronPriority,output_file):
     #Inserts a patron into the book's reservation queue.#
        patron = Patron(patronId, patronPriority)
        existing_patrons = [p for p in self.reservationHeap.get_all_elements() if p.patronId == patronId]
        if existing_patrons:
            already_reserved_patron = existing_patrons[0]
            already_reserved_patron.patronPriority = patronPriority
            print(f"Book {self.bookId} Reservation Updated for Patron {patronId} \n")
        else:
            output_file.write(f"Book {self.bookId} Reserved By Patron {patronId} \n")
            self.reservationHeap.insert(patron)

    def borrowBook(self, patronId, patronPriority,output_file):
    # Borrow a book for a patron
        if self.borrowedBy is None:
        # If the book is not already borrowed, assign it to the current patron
            self.borrowedBy = patronId
            self.availabilityStatus = "No"
            output_file.write(f"Book {self.bookId} Borrowed By Patron {self.borrowedBy}\n")
        else:
         # If the book is already borrowed, add the patron to reservations
            self.__insert_into_reservation(patronId, patronPriority,output_file)
    def returnBook(self, patronId,output_file):
    # Return a borrowed book and handle reservations
        if self.borrowedBy == patronId:
         # If the book is indeed borrowed by the specified patron
            output_file.write(f"Book {self.bookId} Returned By Patron {self.borrowedBy}\n")
            # Check if there are reservations
            if not self.reservationHeap.is_empty():
                next_patron = self.reservationHeap.remove_min()
                self.borrowedBy = next_patron.patronId
                output_file.write(f"Book {self.bookId} Allotted to Patron {self.borrowedBy}\n")
            else:
               # If no reservations, mark the book as available
                self.borrowedBy = None
                self.availabilityStatus = 'Yes'
        else:
        # If the book is not borrowed by the specified patron, return an error message
            return(f"Book {self.bookId} not borrowed by Patron {patronId}\n")
            
class RedBlackTree():
 # Initialize the Red-Black Tree with a sentinel node and set initial properties
    def __init__(self):
        self.TNULL = Book(0, '', '', '')
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.colorFlip = 0
        self.reservationHeap = MinHeap()
    # Search the tree for a specific book ID
    def __search_tree_helper(self, node, key) -> Book:
        if node == self.TNULL or key == node.bookId:
            return node
        if key < node.bookId:
            return self.__search_tree_helper(node.left, key)
        return self.__search_tree_helper(node.right, key)
    # Balancing the tree after deletion
    def __delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    self.colorFlip+=2
                    s.color = 0
                    x.parent.color = 1
                    self.__left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0:
                    self.colorFlip+=1
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        self.colorFlip+=2
                        s.left.color = 0
                        s.color = 1
                        self.__right_rotate(s)
                        s = x.parent.right
                    self.colorFlip+=2
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.__left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    self.colorFlip+=2
                    s.color = 0
                    x.parent.color = 1
                    self.__right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == 0 and s.right.color == 0:
                    self.colorFlip+=1
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        self.colorFlip+=2
                        s.right.color = 0
                        s.color = 1
                        self.__left_rotate(s)
                        s = x.parent.left
                    self.colorFlip+=2
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.__right_rotate(x.parent)
                    x = self.root
        x.color = 0
        # Replace one subtree with another during deletion
    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
        
    # Node deletion
    def __delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.bookId == key:
                z = node
            if node.bookId <= key:
                node = node.right
            else:
                node = node.left
        if z == self.TNULL:
            print("Cannot find key in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.__minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__delete_fix(x)
            
    # Balance the tree after insertion
    def __fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    self.colorFlip+=3
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.__right_rotate(k)
                    self.colorFlip+=2
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.__left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    self.colorFlip+=3
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.__left_rotate(k)
                    self.colorFlip+=2
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.__right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
        
    # Find the node with the minimum key in the subtree rooted at the given node
    def __minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node
    # Perform a left rotation operation on the tree
    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    # Perform a right rotation operation on the tree
    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        # Find the closest node to a given book ID
    def __closest_node(self, node, bookId, min_diff, min_diff_book):
        if node == self.TNULL:
            return
        if node.bookId == bookId:
            min_diff_book[0] = node
            return
        # update min_diff and min_diff_key by
        # checking current node value
        if min_diff > abs(node.bookId - bookId):
            min_diff = abs(node.bookId - bookId)
            min_diff_book[0] = node
        # if k is less than ptr->key then move
        # in left subtree else in right subtree
        if bookId < node.bookId:
            self.__closest_node(node.left, bookId, min_diff, min_diff_book)
        else:
            self.__closest_node(node.right, bookId, min_diff, min_diff_book)
        return min_diff_book[0]
    def findClosestBook(self, targetId):
    # Find the closest book
        closest_book = self.__find_closest_node(self.root, targetId, None)
        if closest_book is None:
            print("No books found in the tree.")
            return []

        # Check for ties
        closest_books = [closest_book]
        distance = abs(closest_book.bookId - targetId)
        self.__find_ties(self.root, targetId, distance, closest_books)

        # Sort by book IDs if there are ties
        closest_books.sort(key=lambda book: book.bookId)

        # Create a list of strings representing the closest book(s)
        closest_books_str = [book._str_() for book in closest_books]

        return closest_books_str
    
    """Recursively finds the closest book node to a given target book ID.

    Args:
        node (Book): The current node in the Red-Black Tree.
        targetId (int): The target book ID.
        currentClosest (Book or None): The currently closest book node.

    Returns:
        Book or None: The closest book node to the target book ID."""
    #
    # Find the closest book(s) to a target book ID
    def __find_closest_node(self, node, targetId, currentClosest):
        if node == self.TNULL:
            return currentClosest
        # Update the closest node if the current node is closer than the previous closest
        if currentClosest is None or abs(node.bookId - targetId) < abs(currentClosest.bookId - targetId):
            currentClosest = node
        # Continue traversing the tree based on the target book ID's position relative to the current node's ID
        if node.bookId > targetId:
            return self.__find_closest_node(node.left, targetId, currentClosest)
        else:
            return self.__find_closest_node(node.right, targetId, currentClosest)
            
    """Recursively finds ties for the closest book in the tree.

    Args:
        node (Book): The current node in the Red-Black Tree.
        targetId (int): The target book ID.
        distance (int): The distance between the current node's ID and the target book ID.
        closestBooks (list[Book]): The list of closest books found so far.

    Returns:
        None
    #
    # Helper function to find ties for the closest book"""
    def __find_ties(self, node, targetId, distance, closestBooks):
    # Base case: Reached the sentinel node
        if node == self.TNULL:
            return
        currentDistance = abs(node.bookId - targetId)
        # Check if the current node has the same distance to the target ID as the closest book
        if currentDistance == distance and node not in closestBooks:
            closestBooks.append(node)
        self.__find_ties(node.left, targetId, distance, closestBooks)
        self.__find_ties(node.right, targetId, distance, closestBooks)
    
    """Inserts a new book with the specified details into the Red-Black Tree.

    Args:
        bookId (int): The ID of the book to insert.
        bookName (str): The name of the book to insert.
        authorName (str): The author of the book to insert.
        availabilityStatus (bool): The availability status of the book to insert (True - available, False - borrowed).

    Returns:
        None
    #"""
    def insertBook(self, bookId, bookName, authorName, availabilityStatus):
     # Create a new book node with the provided details
        book = Book(bookId, bookName, authorName, availabilityStatus)
         # Initialize the new book node's parent, left, and right pointers
        book.parent = None
        book.left = self.TNULL
        book.right = self.TNULL
         # Initially set the color of the new node to red
        book.color = 1
        # Temporary variable to track the parent node during insertion
        y = None
        x = self.root
        # Find the appropriate position for the new book node by traversing the tree
        while x != self.TNULL:
            y = x
            if book.bookId < x.bookId:
                x = x.left
            else:
                x = x.right
        book.parent = y
        if y == None:
            self.root = book
        elif book.bookId < y.bookId:
            y.left = book
        else:
            y.right = book
        if book.parent == None:
            book.color = 0
            return
        if book.parent.parent == None:
            return
        self.__fix_insert(book)
        
        # Find the book in the tree with the given bookId
    def deleteBook(self, bookId, output_file):
        book = self.searchBook(bookId)
        res=""
        if book:
         # Get a string representation of patron IDs in reservations
            reservations_str = ", ".join([str(patron.patronId) for patron in book.reservationHeap.get_all_elements()])
            # Check if there are multiple reservations
            if len(reservations_str)>1: 
             # Notify about book unavailability and cancel reservations
                output_file.write(f"Book {book.bookId} is no longer available. Reservations made by Patrons {reservations_str} have been cancelled!\n\n")
            else:
             # Notify about book unavailability
                output_file.write(f"Book {book.bookId} is no longer available.\n\n")
                
                 # Delete the book node from the Red-Black Tree
            self.__delete_node_helper(self.root, bookId)
        return res
    def searchBook(self, bookId):
     # Search the Red-Black Tree for a book with the given bookId
        return self.__search_tree_helper(self.root, bookId)
    def printBook(self, bookId):
     # Search for the book with the given bookId in the Red-Black Tree
        book = self.__search_tree_helper(self.root, bookId)
        # Check if the book is not the sentinel node (TNULL)
        if book != self.TNULL:  # Check if the book is not the sentinel node
            return book
    def printBooks(self, bookId1, bookId2):
        arr=[]
        # Iterate through book IDs in the specified range
        for bookId in range(bookId1, bookId2+1):
         # Check if the book with the current ID exists in the tree
            if self.printBook(bookId) is not None:
             # Append the book to the result array
                arr.append(self.printBook(bookId))
        return arr
    def borrowBook(self, patronId, bookId, patronPriority,output_file):
     # Find the book in the tree with the given bookId
        book = self.searchBook(bookId)
        if (book):
         # Borrow the book by updating reservations
            book.borrowBook(patronId, patronPriority,output_file)
        return str(book)
    def returnBook(self, patronId, bookId,output_file):
     # Find the book in the tree with the given bookId
        book = self.searchBook(bookId=bookId)
        if (book):
        # Return the book and manage reservations
            book.returnBook(patronId,output_file)
        return str(book)
    def colorFlipCount(self):
     # Print the total number of color flips
        print(self.colorFlip)
        return(f"Colour Flip Count: {self.colorFlip}\n")
    def in_order_helper(self, node: Book):
        transformations = 0
        if node != self.TNULL:
         # Traverse the left subtree
            transformations += self.in_order_helper(node.left)
            # Count transformations for black nodes
            if node.color == 0:  # Only count transformations for black nodes
                transformations += node.transformations
                 # Traverse the right subtree
            transformations += self.in_order_helper(node.right)
        return transformations
    def quit(self):
    # Notify that the program is terminated
        print("Program Terminated!!")

# Create an instance of the Red-Black Tree
gator_library = RedBlackTree()

if len(sys.argv) < 2:
    print("Please provide the input file path as a command-line argument.")
    exit()
input_file_path = sys.argv[1]
# Remove the extension from the input file path
input_file_base_name, extension = os.path.splitext(input_file_path)

output_file_name = f"{input_file_base_name}_output_file.txt"

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_name, 'w') as output_file:
 # Iterate through each line in the input file
    for line in input_file:
        input_line = line.strip()
        in_params = input_line[input_line.find("(") + 1:input_line.find(")")].split(",")
        #print(in_params)
       # print(input_line)
        # Check the command type and perform corresponding operations
        if input_line.startswith("InsertBook"):
            book_id = int(in_params[0].strip())
            book_name = in_params[1].strip()  # assuming the book name is within quotes
            author_name = in_params[2].strip()  # assuming the author name is within quotes
            availability_status = in_params[3].strip()  # assuming the status is within quotes
           # print(book_id,book_name,author_name,availability_status)
            node = gator_library.insertBook(book_id, book_name, author_name, availability_status)
            # Assuming the insertBook method does not return any value
            
            #output_file.write(f"Book {book_id} inserted\n\n")
            #output_file.write("\n")
        elif input_line.startswith("PrintBook"):
            if len(in_params) == 1:
                book_id = int(in_params[0].strip())
                book = gator_library.searchBook(book_id)
                if book != gator_library.TNULL:  # Check if the book is not the sentinel node
                    output_file.write(book._str_())
                else:
                    output_file.write(f"Book {book_id} not found in the Library")
                output_file.write("\n\n")
            
            else:
                book_id1 = int(in_params[0].strip())
                print(book_id1)
                book_id2 = int(in_params[1].strip())
                arr=gator_library.printBooks(book_id1, book_id2)
                # Assuming printBooks directly prints to the console.
                for i in arr:
                    output_file.write(i._str_())
                ##output_file.write("Printed books in range\n\n")
                    output_file.write("\n\n")
        elif input_line.startswith("BorrowBook"):
            patron_id = int(in_params[0].strip())
            book_id = int(in_params[1].strip())
            patron_priority = int(in_params[2].strip())
            
            gator_library.borrowBook(patron_id, book_id, patron_priority, output_file)
            # Assuming borrowBook method does not return any value
            # output_file.write(f"Book {book_id} borrowed by Patron {patron_id}\n\n")
            #output_file.write("\n")

        elif input_line.startswith("ReturnBook"):
            patron_id = int(in_params[0].strip())
            book_id = int(in_params[1].strip())
            gator_library.returnBook(patron_id, book_id,output_file)
            # Assuming returnBook method does not return any value
            #output_file.write(f"Book {book_id} returned by Patron {patron_id}\n\n")
            #output_file.write("\n")

        elif input_line.startswith("FindClosestBook"):
            target_id = int(in_params[0].strip())
            p=gator_library.findClosestBook(target_id)
            for i in p:
                output_file.write(i)
                output_file.write("\n\n")
            # Assuming findClosestBook directly prints to the console.

        elif input_line.startswith("DeleteBook"):
            book_id = int(in_params[0].strip())
            gator_library.deleteBook(book_id,output_file)
            # Assuming deleteBook method does not return any value
            #output_file.write("\n")

        elif input_line.startswith("ColorFlipCount"):
            output_file.write(gator_library.colorFlipCount())
            # Assuming colorFlipCount directly prints to the console.
            #output_file.write("Color flip count displayed\n\n")
            output_file.write("\n")

        elif input_line.startswith("Quit"):
            output_file.write("Program Terminated!!\n")
            break
