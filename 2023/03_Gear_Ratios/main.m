clc
clear

file = fopen("input.txt",'r');
A = strsplit(fscanf(file, "%c"))';

fclose(file);

symbolIndicies = [];
numberIndicies = [];
gearIndicies = [];

for iRow = 1:size(A,1)
    row = A{iRow};
    

    prevNumber = false;
    startIndex = 1;
    endIndex = length(row);
    for iChar = 1:endIndex
        charIsNumber = isstrprop(row(iChar), 'digit');
        charIsSymbol = (row(iChar) ~= '.' & ~charIsNumber);
        charIsGearSymbol = row(iChar) == '*';

        if (prevNumber && ~charIsNumber)
            % Om förra är nummer men denna inte
            % Lägg till slutindex
            % Lägg till i listan
            numberIndicies = [[iRow,startIndex,iChar-1]; numberIndicies];
    
        elseif (charIsNumber)
            if ~prevNumber
                startIndex = iChar;
            end
            
        end

        if charIsSymbol
            symbolIndicies = [[iRow, iChar]; symbolIndicies];
        end

        if charIsGearSymbol
            gearIndicies =  [[iRow, iChar]; gearIndicies];
        end

        prevNumber = charIsNumber;
    end

    if prevNumber
        numberIndicies = [[iRow,startIndex,length(row)]; numberIndicies];
    end
end

totalSum = 0;

for iNumber = 1:size(numberIndicies,1)
    rowNumber = numberIndicies(iNumber,1);
    startIndex = numberIndicies(iNumber,2);
    endIndex = numberIndicies(iNumber,3);

    isInRange = (symbolIndicies(:,2)<= endIndex + 1) + (symbolIndicies(:,2) >= startIndex - 1);
    isInCloseRow = abs(symbolIndicies(:,1) -rowNumber) < 2;

    isAdjacent = isInRange + isInCloseRow == 3;
    
    shouldAdd = sum(isAdjacent) > 0;

    if shouldAdd
        numString = A{rowNumber}(startIndex:endIndex);


        totalSum = totalSum + str2num(numString);
    end

end

totalSum


gearSum = 0;
for iGear = 1:size(gearIndicies,1)
    rowNumber = gearIndicies(iGear,1);
    rowIndex = gearIndicies(iGear,2);



    isInRange = (numberIndicies(:,2)-1 <= rowIndex) +  (rowIndex <= numberIndicies(:,3) + 1);
    isInCloseRow = abs(numberIndicies(:,1) - rowNumber) < 2;

    isAdjacent = isInRange + isInCloseRow == 3;
    
    shouldAdd = sum(isAdjacent) == 2;

    if shouldAdd
        numbers = numberIndicies(isAdjacent,:);
        

        num1 = str2double(A{numbers(1,1)}(numbers(1,2):numbers(1,3)));
        num2 = str2double(A{numbers(2,1)}(numbers(2,2):numbers(2,3)));


        gearSum = gearSum + num1*num2;
    end

end

gearSum