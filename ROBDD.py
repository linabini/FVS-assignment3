

class ROBDD:
    def __init__(self):
        # Unique table: {(var, low, high): id}
        self.unique_table = {}
        # Reverse lookup: {id: (var, low, high)}
        self.nodes = {0: "False", 1: "True"}
        self.next_id = 2

    def get_node(self, var, low, high):
        """Implements the reduction rules."""
        if low == high:
            return low
        if (var, low, high) in self.unique_table:
            return self.unique_table[(var, low, high)]
        
        node_id = self.next_id
        self.unique_table[(var, low, high)] = node_id
        self.nodes[node_id] = (var, low, high)
        self.next_id += 1
        return node_id

    def build(self, formula, vars_order):
        """Recursively builds the BDD using Shannon Expansion."""
        if formula == "0": return 0
        if formula == "1": return 1
        if not vars_order:
            return 1 if eval(formula) else 0

        var = vars_order[0]
        remaining_vars = vars_order[1:]

        # Shannon Expansion: f = (var' * f[var=0]) + (var * f[var=1])
        low_formula = formula.replace(var, "0")
        high_formula = formula.replace(var, "1")
        
        # Simplify strings for eval-friendliness (basic logic gates)
        def simplify(f):
            try: return str(int(eval(f.replace('AND', '&').replace('OR', '|').replace('NOT', '~'))))
            except: return f

        low_node = self.build(simplify(low_formula), remaining_vars)
        high_node = self.build(simplify(high_formula), remaining_vars)

        return self.get_node(var, low_node, high_node)

    def save_structure(self, filename="robdd_output.txt"):
        with open(filename, "w") as f:
            f.write("ROBDD Structure:\n")
            for nid in sorted(self.nodes):
                val = self.nodes[nid]
                if nid in [0, 1]:
                    f.write(f"  {nid}: {val}\n")
                else:
                    var, low, high = val
                    f.write(f"  {nid}: If {var} then High->{high} else Low->{low}\n")
        print(f"ROBDD structure saved to {filename}")

# Example
# Formula: (A AND B) OR C
bdd = ROBDD()
order = ["A", "B", "C"]
# Python-friendly logic syntax
formula = "(A & B) | C"
root = bdd.build(formula, order)
bdd.save_structure()