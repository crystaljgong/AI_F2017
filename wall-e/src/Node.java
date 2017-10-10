
import java.awt.Point;

public class Node extends Point implements Comparable<Node> {

	int fromStart_g;
	int fromEnd_h;
	int fTotal;
	Node parent;

	public Node(Point p, Node from) {
		super(p);
		this.fromStart_g = ((from == null) ? 0 : from.getFromStart_g() + 1);
		this.fromEnd_h = 0;
		this.fTotal = 0;
		this.parent = from;
	}


	@Override
	public String toString() {
		if (parent != null) {
			return "\nNode [fTotal=" + fTotal + ", parent=" + parent.getLocation() + ", location=" + super.toString() + "]";
	
		}
		else
			return "\nNode [fTotal=" + fTotal + ", location=" + super.toString() + "]";
	}
			
	public int getFromStart_g() {
		return fromStart_g;
	}

	public void setFromStart_g(int fromStart_g) {
		this.fromStart_g = fromStart_g;
		updatefTotal();
	}

	public int getFromEnd_h() {
		return fromEnd_h;
	}

	public void setFromEnd_h(int fromEnd_h) {
		this.fromEnd_h = fromEnd_h;
		updatefTotal();
	}

	public int getfTotal() {
		return fTotal;
	}

	public void updatefTotal() {
		this.fTotal = this.fromEnd_h + this.fromStart_g;
	}

	public Node getParent() {
		return parent;
	}

	public void setParent(Node cameFrom) {
		this.parent = cameFrom;
	}

	@Override
	public int compareTo(Node o) {
		if (this.fTotal > o.getfTotal()) return 1;
		else if (this.fTotal == o.getfTotal()) return 0;
		else return -1;
	}

	@Override
	public boolean equals(Object o) {
		if (o instanceof Node) {
		return (this.getLocation().equals(((Node) o).getLocation())); //same point
			//&& this.getfTotal() == ((Node)o).getfTotal()); //same f score
		}
		return false;
	}
	
	@Override
    public int hashCode() {
		return super.hashCode()*fTotal;
        
    }

}
