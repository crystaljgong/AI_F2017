
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
	PriorityQueue<Node> open = new PriorityQueue<Node>();
	Stack<Point> path = new Stack<Point>();


	public int calcDistance(Point current, Point end, int heuristic) {
		double dx = Math.abs(current.getX() - end.getX());
		double dy = Math.abs(current.getY() - end.getY());
		if (heuristic == 0) {
			//manhattan distance
			return (int) (dx + dy);
		} else if (heuristic==1) {
			//euclidean distance
			return (int) Math.sqrt(dx*dx+dy*dy);
		}
		else 
			// diagonal distance
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
		}
		return neighbors;
	}

	public void generatePathAndGo(Node end) {
		path.push(end.getLocation());

		Node parent = end.getParent();

		// push successive parent onto stack
		while (!(parent.getLocation().equals(startPos))) {

			path.push(parent.getLocation());
			parent = parent.getParent();
			if (parent == null) {
				break;
			}
		}

		// move along the path we created after generate path
		while (!path.isEmpty()) {
			Point nextMove = path.pop();
			if (!super.pingMap(nextMove).equals("X")) {
				super.move(nextMove);
				try {
					TimeUnit.SECONDS.sleep((long) 0.5);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			} else {
				break;
			}
		}
	}

	@Override
	public void travelToDestination() {

		if (isUncertain) {
			while(!super.getPosition().equals(endPos)) {
				aStarCertain();
			}
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
		startPos = start.getLocation();

		whileopen: while (!open.isEmpty()) {

			// get neighbors
			Node center = open.poll();
			Node[] neighbors = getNeighbors(center);

			for (Node n : neighbors) {

				// check if neighbor is off edge of map
				if ((n.getX() >= 0 && n.getY() >= 0 && n.getX() < height && n.getY() < width)) {

					// check if this neighbor is the end
					if (n.getLocation().equals(endPos)) {
						generatePathAndGo(n);
						break whileopen; // break this while loop
					}
					

					// check if it's an obstacle
					boolean obs = false;
					if (isUncertain) {
						int obstacle = 0;
						int notObstacle = 0;
						int times = 0;

						if ((width * height)/4 < 40) {
							times = 40;
						} else {
							times = (width * height)/4;
						}
						
						for (int z = 0; z < times; z++) {
							if (super.pingMap(new Point((int) n.getX(), (int) n.getY())).equals("O")) {
								notObstacle += 1;
							} else {
								obstacle += 1;
							}
						}
						if (obstacle > notObstacle) {
							obs = true;
						}
					} else {
						obs = !super.pingMap(new Point((int) n.getX(), (int) n.getY())).equals("O");
					}
					
					if (!obs) {

						// set f score for neighbor
						n.setFromStart_g(center.fromStart_g + 1);
						n.setFromEnd_h(calcDistance(n, endPos, 1));

						// check if neighbor gives a better path than anything else we've seen already
						boolean skip = false;
						for (Node o : open) {
							// if a node with the same position as successor is in the OPEN list which has a
							// lower f than successor, skip this successor
							if (o.getLocation().equals(n.getLocation()) && (o.getfTotal() <= n.getfTotal())) {
								skip = true;
							}
							// if a node with the same position as successor has onList flag which has
							// a lower f than successor, skip this successor
							if(o.getLocation().equals(n.getLocation()) && (o.getfTotal() <= n.getfTotal()) && o.getOnList()) {
								skip = true;
							}
						}
						
						// otherwise, add the node to the open list
						if (!skip) {
							open.add(n);
						}

					}
				} 
			}

			center.setOnList();

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
			World myWorld = new World("TestCases/myInputFile1.txt", false);

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
