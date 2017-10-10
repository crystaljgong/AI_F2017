
//Crystal Gong (cjg5uw) and Cynthia Zheng (xz7uy)
import world.Robot;
import world.World;

import java.awt.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class MyRobot extends Robot {
	boolean isUncertain = false;
	Point startPos;
	Point endPos;
	int height;
	int width;
	HashSet<Node> closed = new HashSet<Node>();
	PriorityQueue<Node> open = new PriorityQueue<Node>();
	Stack<Point> path = new Stack<Point>();


	public int calcDistance(Point current, Point end) {
		// using diagonal distance
		double dx = Math.abs(current.getX() - end.getX());
		double dy = Math.abs(current.getY() - end.getY());
		return (int) Math.max(dx, dy);
	}
	
	public Node[] getNeighbors(Node n) {
		int translations[][] = { { 0, 1 }, { 1, 1 }, { 1, 0 }, { 1, -1 }, { 0, -1 }, { -1, -1 }, { -1, 0 }, { -1, 1 } };
		/*
		 * Numbers below correspond to indices in translations[][] 5 6 7 4 p 0 3 2 1
		 */
		// set location to be same as parent for now
		Node[] neighbors = { new Node(n.getLocation(), n), new Node(n.getLocation(), n), new Node(n.getLocation(), n),
				new Node(n.getLocation(), n), new Node(n.getLocation(), n), new Node(n.getLocation(), n),
				new Node(n.getLocation(), n), new Node(n.getLocation(), n) };

		for (int i = 0; i < neighbors.length; i++) {
			neighbors[i].translate(translations[i][0], translations[i][1]); // make new pt
			// System.out.println("i: " + i + ", " + neighbors[i]);
		}
		return neighbors;
	}

	public void generatePathAndGo(Node end) {
		path.push(end.getLocation());

		Node parent = end.getParent();

		// push successive parent onto stack
		while (!parent.getLocation().equals(startPos)) {
			System.out.println("parent: " + parent);
			path.push(parent.getLocation());
			parent = parent.getParent();
		}
		// print the stack
		System.out.println(Arrays.toString(path.toArray()));

		// move along the path we created after generate path
		while (!path.isEmpty()) {
			super.move(path.pop());
			try {
				TimeUnit.SECONDS.sleep((long) .5);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	@Override
	public void travelToDestination() {

		if (isUncertain) {
			// call function to deal with uncertainty
		} else {
			aStarCertain();
			// call function to deal with certainty
		}
	}

	public void aStarCertain() {
		// init with starting point
		Node start = new Node(super.getPosition(), null);
		open.add(start);

		whileopen: while (!open.isEmpty()) {

			// get neighbors
			Node center = open.poll();
			System.out.println("\n THE CENTER IS " + center.getLocation() + "\n");
			Node[] neighbors = getNeighbors(center);

			for (Node n : neighbors) {
				System.out.println("LOOKING AT " + n.getLocation());

				// check if neighbor is off edge of map
				if ((n.getX() >= 0 && n.getY() >= 0 && n.getX() < height && n.getY() < width)) {
					// System.out.println(n.toString() + " is within bounds");

					// check if this neighbor is the end
					if (n.getLocation().equals(endPos)) {
						System.out.println("FOUND THE END!!!!");
						generatePathAndGo(n);
						break whileopen; // break this while loop
					}

					// check if it's an obstacle
					if (super.pingMap(new Point((int) n.getX(), (int) n.getY())).equals("O")) {

						// set f score for neighbor
						n.setFromStart_g(center.fromStart_g + 1);
						n.setFromEnd_h(calcDistance(n, endPos));

						// check if neighbor gives a better path than anything else we've seen already
						boolean skip = false;
						for (Node o : open) {
							// if a node with the same position as successor is in the OPEN list which has a
							// lower f than successor, skip this successor
							if (o.getLocation().equals(n.getLocation()) && (o.getfTotal() <= n.getfTotal())) {
								System.out.println("skip is true! open's  f: " + o.getfTotal());
								System.out.println("my f (open): " + n.getfTotal());
								skip = true;
							}
						}
						for (Node other : closed) {
							// if a node with the same position as successor is in the CLOSED list which has
							// a lower f than successor, skip this successor
							if (other.getLocation().equals(n.getLocation()) && (other.getfTotal() <= n.getfTotal())) {
								System.out.println("skip is true! closed's  f: " + other.getfTotal());
								System.out.println("my f (closed): " + n.getfTotal());
								skip = true;
							}
						}
						// otherwise, add the node to the open list
						if (!skip) {
							System.out.println("adding " + n.getLocation() + " to open list with f " + n.getfTotal());
							open.add(n);
						}

					} else
						System.out.println("ping for " + n.getLocation() + " gave not O");

				} else
					System.out.println("point " + n.getLocation() + " out of bounds");

			}
			// the following can be erased after debugging is finished
			System.out.println("OPEN LIST: ");
			for (Node thing : open) {
				System.out.println(thing);
			}

			closed.add(center);

			System.out.println("CLOSED LIST: ");
			for (Node thing : closed) {
				if (thing.getParent() != null) {
					System.out.println(thing);// + " coming from " + thing.getParent());
				}
			}
		}

	}

	public void setHeight(int height) {
		this.height = height;
	}

	public void setWidth(int width) {
		this.width = width;
	}

	public void setStartPos(Point startPos) {
		this.startPos = startPos;
	}

	public void setEndPos(Point endPos) {
		this.endPos = endPos;
	}

	@Override
	public void addToWorld(World world) {
		isUncertain = world.getUncertain();
		super.addToWorld(world);
	}

	public static void main(String[] args) {
		try {
			World myWorld = new World("TestCases/myInputFile4.txt", false);

			MyRobot robot = new MyRobot();
			robot.addToWorld(myWorld);
			myWorld.createGUI(400, 400, 200); // uncomment this and create a GUI; the last parameter is delay in msecs

			robot.setStartPos(myWorld.getStartPos());
			robot.setEndPos(myWorld.getEndPos());
			robot.setHeight(myWorld.numRows());
			robot.setWidth(myWorld.numCols());
			robot.travelToDestination();

		}

		catch (Exception e) {
			e.printStackTrace();
		}
	}

}
