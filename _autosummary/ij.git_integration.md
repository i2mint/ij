# ij.git_integration

Git integration for diagram version control and diffing.

Provides tools for comparing diagrams, merging changes, and tracking history.

### Classes

| [`DiagramChanges`](#ij.git_integration.DiagramChanges)([added_nodes, removed_nodes, ...])   | Changes between two diagrams.                |
|------------------------------------------------------------------------------------------------------|----------------------------------------------|
| [`DiagramDiff`](#ij.git_integration.DiagramDiff)()                                       | Compare and diff diagrams.                   |
| [`DiagramHistory`](#ij.git_integration.DiagramHistory)()                                    | Track diagram history and changes over time. |

### *class* ij.git_integration.DiagramChanges(added_nodes=<factory>, removed_nodes=<factory>, modified_nodes=<factory>, added_edges=<factory>, removed_edges=<factory>, modified_edges=<factory>)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Changes between two diagrams.

#### *property* has_changes *: [bool](https://docs.python.org/3/builtins/functions.html#bool)*

Check if there are any changes.

#### *property* total_changes *: [int](https://docs.python.org/3/builtins/functions.html#int)*

Count total number of changes.

### *class* ij.git_integration.DiagramDiff

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Compare and diff diagrams.

#### compare(diagram1, diagram2)

Compare two diagrams.

* **Parameters:**
  * **diagram1** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Original diagram
  * **diagram2** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Modified diagram
* **Return type:**
  [`DiagramChanges`](#ij.git_integration.DiagramChanges)
* **Returns:**
  DiagramChanges describing differences

### Example

```pycon
>>> differ = DiagramDiff()
>>> changes = differ.compare(old_diagram, new_diagram)
>>> print(f"Added: {len(changes.added_nodes)} nodes")
```

#### compare_files(file1, file2)

Compare two diagram files.

* **Parameters:**
  * **file1** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to first diagram
  * **file2** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to second diagram
* **Return type:**
  [`DiagramChanges`](#ij.git_integration.DiagramChanges)
* **Returns:**
  DiagramChanges describing differences

#### generate_diff_report(changes)

Generate human-readable diff report.

* **Parameters:**
  **changes** ([`DiagramChanges`](#ij.git_integration.DiagramChanges)) – DiagramChanges to report
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Formatted diff report string

#### merge(base, branch1, branch2, strategy='union')

Merge two diagram versions with a common base.

* **Parameters:**
  * **base** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Common ancestor diagram
  * **branch1** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – First modified version
  * **branch2** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – Second modified version
  * **strategy** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Merge strategy (‘union’, ‘intersection’, ‘ours’, ‘theirs’)
* **Return type:**
  [`DiagramIR`](ij.core.md#ij.core.DiagramIR)
* **Returns:**
  Merged DiagramIR

### Example

```pycon
>>> differ = DiagramDiff()
>>> merged = differ.merge(base, branch1, branch2, strategy='union')
```

### *class* ij.git_integration.DiagramHistory

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Track diagram history and changes over time.

#### add_version(name, diagram)

Add a version to history.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Version name/identifier
  * **diagram** ([`DiagramIR`](ij.core.md#ij.core.DiagramIR)) – DiagramIR snapshot

#### compare_versions(name1, name2)

Compare two versions.

* **Parameters:**
  * **name1** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – First version name
  * **name2** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Second version name
* **Return type:**
  [`DiagramChanges`](#ij.git_integration.DiagramChanges)
* **Returns:**
  DiagramChanges between versions

#### get_changelog()

Generate changelog across all versions.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Formatted changelog string

#### get_version(name)

Get a specific version.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Version name
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`DiagramIR`](ij.core.md#ij.core.DiagramIR)]
* **Returns:**
  DiagramIR if found, None otherwise

#### list_versions()

List all version names.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
