def dumpKbStatistics(kbPath):
    """
    Function to calculate the statistics of a given KB.

    Parameters:
        kbPath:     the input KB path. KB is in the Numerated Format.
        outputPath: The output path for the statistics file, in Excel spreadsheet format.
                    The file should be at the same path with the KB, and the name of the file
                    should be: <KB name>_statistics.xlsx
    
    Returns:
        None

    An Excel file should be written in the directory 'kbPath'.
    The Excel spreadsheet file should contain the following sheets:
        - Overview:
            - 1st row, the title row:
                - KB: the name of the KB
                - #relations: the number of different relations
                - #entities: the number of different entities
                - #classes: the number of classes in the KB
                - avg. degr.: the average degree of entities in the KB
            - 2nd row is for the corresponding values
        - Relations:
            - 1st row, the title row:
                - relation: the relation name
                - id: mapped numerical id of the relation
                - #instances: the number of records/triples in this relation
                - prop. (%): the proportion of the relation in the entire KB, round to 2 decimal places
                - property: whether the relation is a property
                - reified: whether the relation is based on reified records/triples
                - #entities: the number of different entities involved in the relation
                - #subjects: the number of different subjects involved in the relation
                - #objects: the number of different objects involved in the relation
                - functionality: the functionality value of the relation, round to 2 decimal places
                - symmetricity: the proportion of symmetric pairs in the relation, round to 2 decimal places
            - other rows are the statistics of each relation
    """
    raise Exception("Not Implemented")