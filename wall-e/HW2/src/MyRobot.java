
import world.Robot;
import world.World;

import java.awt.*;
import java.util.*;

public class MyRobot extends Robot {
	boolean isUncertain = false;
	Point startPos;
	Point endPos;
	int lowestCost = 0;
	int distToGoal;
	int height;
	int width;
	HashSet closed;
	PriorityQueue<Node> open = new PriorityQueue<Node>();

	public Node[] getNeighbors(Node n) {
		int translations[][] = { { -1, 0 }, { -1, 1 }, { 0, 1 }, { 1, 1 }, { 1, 0 }, { 1, -1 }, { 0, -1 }, { -1, -1 } };

		/*
		 * Numbers below correspond to indices in translations[][] 7 0 1 6 p 2 5 4 3
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

	@Override
	public void travelToDestination() {

		// init with starting point
		Node start = new Node(super.getPosition(), null);
		open.add(start);

		// get neighbors
		Node center = open.poll();

		Node[] neighbors = getNeighbors(center);
		// Integer.MAX_VALUE; for infinity distance

		for (Node n : neighbors) { 
			// check if off edge of map
			if ((n.getX() >= 0 && n.getY() >= 0 && n.getX() < height && n.getY() < width)) {
				System.out.println(n.toString() + " is within bounds");
				//check if not an obstacle
				if (super.pingMap(new Point((int) n.getX(), (int) n.getY())).equals("O")) {
					System.out.println(n.toString() + " is O");

					 //set f score for neighbor
					 n.setFromStart_g(center.fromStart_g + 1);
					 n.setFromEnd_h(calcDistance(n, endPos));
					
					
					
					// if a node with the same position as
					// successor is in the CLOSED list which has
					// a lower f than successor, skip this successor
					// otherwise, add the node to the open list
					 boolean skip = false;
					 for (Node other : open) {
						// if a node with the same position as
							// successor is in the OPEN list which has a
							// lower f than successor, skip this successor
						 if (other.getLocation().equals(n.getLocation()) && (other.getfTotal() < n.getfTotal())) {
							 System.out.println("other f: " + other.getfTotal());
							 System.out.println("this f: " + n.getfTotal());
						 }
					 }
				}

			}

		}

		// int size = open.size();
		// for (int i = 0; i<size; i++) {
		// System.out.println(open.poll().toString());
		// }

		if (isUncertain) {
			// call function to deal with uncertainty
		} else {

			// call function to deal with certainty
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

	public int calcDistance(Point current, Point end) {
		// using diagonal distance
		double dx = Math.abs(current.getX() - end.getY());
		double dy = Math.abs(current.getY() - end.getY());
		return (int) Math.max(dx, dy);
	}

	@Override
	public void addToWorld(World world) {
		isUncertain = world.getUncertain();
		super.addToWorld(world);
	}

	public static void main(String[] args) {
		try {
			World myWorld = new World("TestCases/myInputFile1.txt", true);

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
