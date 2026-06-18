import {
  Drawer,
  Toolbar,
  List,
  ListItemButton,
  ListItemText
} from "@mui/material";

const drawerWidth = 240;

function AdminSidebar() {

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        "& .MuiDrawer-paper": {
          width: drawerWidth
        }
      }}
    >

      <Toolbar />

      <List>

        <ListItemButton>
          <ListItemText primary="Dashboard" />
        </ListItemButton>

        <ListItemButton>
          <ListItemText primary="Users" />
        </ListItemButton>

        <ListItemButton>
          <ListItemText primary="Villages" />
        </ListItemButton>

        <ListItemButton>
          <ListItemText primary="Farmers" />
        </ListItemButton>

        <ListItemButton>
          <ListItemText primary="Wells" />
        </ListItemButton>

        <ListItemButton>
          <ListItemText primary="Reports" />
        </ListItemButton>

        <ListItemButton>
          <ListItemText primary="Settings" />
        </ListItemButton>

      </List>

    </Drawer>
  );
}

export default AdminSidebar;