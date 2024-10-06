class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath:
            self.load_from_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols
            self.matrix = {}

    def load_from_file(self, matrixFilePath):
        with open(matrixFilePath, 'r') as file:
            lines = file.readlines()
        
        self.numRows = int(lines[0].split('=')[1].strip())
        self.numCols = int(lines[1].split('=')[1].strip())
        self.matrix = {}

        for line in lines[2:]:
            line = line.strip()
            if line:
                if not line.startswith('(') or not line.endswith(')'):
                    raise ValueError("Input file has wrong format")
                
                # Parse the tuple (row, col, value)
                values = line[1:-1].split(',')
                row, col, value = int(values[0].strip()), int(values[1].strip()), int(values[2].strip())
                
                # Store in matrix dictionary only if value is non-zero
                if value != 0:
                    self.setElement(row, col, value)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def getElement(self, currRow, currCol):
        return self.matrix.get((currRow, currCol), 0)

    def __add__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition")

        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        
        # Add values from self
        for (i, j), value in self.matrix.items():
            result.setElement(i, j, value + other.getElement(i, j))
        
        # Add values from other matrix that aren't in self
        for (i, j), value in other.matrix.items():
            if (i, j) not in result.matrix:
                result.setElement(i, j, value)
        
        return result

    def __sub__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction")

        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        
        # Subtract values from self
        for (i, j), value in self.matrix.items():
            result.setElement(i, j, value - other.getElement(i, j))
        
        # Subtract values from other matrix that aren't in self
        for (i, j), value in other.matrix.items():
            if (i, j) not in result.matrix:
                result.setElement(i, j, -value)
        
        return result

    def __mul__(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions do not match for multiplication")

        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        
        for (i, k), value in self.matrix.items():
            for j in range(other.numCols):
                result.setElement(i, j, result.getElement(i, j) + value * other.getElement(k, j))
        
        return result


def main():
    matrix1_path = input("Enter the path of the first matrix file: ")
    matrix2_path = input("Enter the path of the second matrix file: ")
    
    matrix1 = SparseMatrix(matrix1_path)
    matrix2 = SparseMatrix(matrix2_path)

    print("Select operation: 1 for addition, 2 for subtraction, 3 for multiplication")
    choice = int(input("Your choice: "))

    if choice == 1:
        result = matrix1 + matrix2
    elif choice == 2:
        result = matrix1 - matrix2
    elif choice == 3:
        result = matrix1 * matrix2
    else:
        print("Invalid choice")
        return
    
    # Save the result to an output file
    with open('output.txt', 'w') as file:
        file.write(f"rows={result.numRows}\n")
        file.write(f"cols={result.numCols}\n")
        for (i, j), value in result.matrix.items():
            file.write(f"({i}, {j}, {value})\n")

if __name__ == "__main__":
    main()
