import { SimpleForm, TextInput, SelectInput, Title, Datagrid, TextField, List, Pagination, Create, Show, TabbedShowLayout, Tab, FunctionField, BooleanField, DateField, SimpleShowLayout, useShowContext, Edit, PasswordInput, BooleanInput, NumberInput, DateTimeInput } from 'react-admin';
import { useState } from 'react';
import { TextField as MuiTextField, Box, Typography, Paper, Stack, Chip, IconButton, InputAdornment } from '@mui/material';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

import { Search as SearchIcon } from '@mui/icons-material';


export const UserCreateForm = () => {
    const default_values = {
        username: null,
        email: null,
        status: 1,
        password: null,
        role: "ROLE_PROVIDER"
    }
    return (
    <Create>
        <SimpleForm defaultValues={default_values} > 
            <TextInput source="username" required />
            <TextInput source="email" type="email" required />
            <SelectInput 
                source="status"
                choices={[
                { id: 1, name: "active" },
                { id: 0, name: "inactive" },
                ]}
            />
            <SelectInput 
                source="role"
                choices={[
                { id: "ROLE_PROVIDER", name: "ROLE_PROVIDER" },
                { id: "ROLE_ADMIN", name: "ROLE_ADMIN" },
                ]}
                required
            />
            <TextInput source="password" type="password" required />
        </SimpleForm>
    </Create>
    );
};

export const UserListPagination = () => (
    <Pagination rowsPerPageOptions={[5, 10, 25, 50, 100]} />
);

const UserListSearch = ({ filter, setFilter }) => {
    return (
        <Box display="flex" alignItems="center" mb={2}>
            <MuiTextField
                label="Search User"
                variant="outlined"
                value={filter}
                onChange={e => setFilter(e.target.value)}
                size="small"
                sx={{ marginRight: 2 }}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <SearchIcon />
                        </InputAdornment>
                    )
                }}
                fullWidth
            />
        </Box>
    );
};

export const UserList = () => {
    const [filter, setFilter] = useState('');

    return (
        <div>
            <Title title="User List" />
            {/* <UserListSearch filter={filter} setFilter={setFilter} /> */}
            <List
                resource="users"
                filter={{ q: filter }}
                pagination={<UserListPagination />}
            >
                <Datagrid rowClick="show">
                    <TextField source="id" label="ID" sortable />
                    <TextField source="username" label="User" sortable />
                    {/* <TextField source="email" label="Email" sortable /> */}
                    
                    <FunctionField render={record => <StatusField record={record} />} label="Status" />

                    <TextField source="role" label="Role" sortable />
                    {/* <TextField source="logged_in" label="Logged In" sortable />
                    <TextField source="failed_login_attempts" label="Failed Login Attempts" sortable /> */}
                    <TextField source="created_at" label="Created at" sortable />
                    <TextField source="updated_at" label="Updated at" sortable />
                    <TextField source="deleted_at" label="Deleted at" sortable />
                </Datagrid>
            </List>
        </div>
    );
};

const StatusField = ({ record }) => {
    if (!record) return null;
    const label = record.status === 1 ? 'Active' : 'Inactive';
    const color = record.status === 1 ? 'success' : 'default';
    return (
        <Chip label={label} color={color} variant="outlined" />
    );
};

const PasswordField = () => {
    const [showPassword, setShowPassword] = useState(false);
    const { record } = useShowContext(); // get the record
    if (!record) return null;

    return (
        <Box display="flex" alignItems="center" gap={1}>
            <Typography>
                {showPassword ? record.password : '••••••••'}
            </Typography>
            <IconButton size="small" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <VisibilityOff fontSize="small" /> : <Visibility fontSize="small" />}
            </IconButton>
        </Box>
    );
};

export const UserShow = () => (
    <Show>
        <SimpleShowLayout>
            <Paper elevation={2} sx={{ p: 4 }}>
                <Typography variant="h5" gutterBottom>User Details</Typography>

                {/* Two columns layout */}
                <Box
                    display="flex"
                    flexDirection={{ xs: 'column', md: 'row' }}
                    gap={4}
                >
                    {/* Left column */}
                    <Box flex={1}>
                        <Stack spacing={3}>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">ID</Typography>
                                <TextField source="id" />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Username</Typography>
                                <TextField source="username" />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Email</Typography>
                                <TextField source="email" />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Role</Typography>
                                <TextField source="role" />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Password</Typography>
                                <PasswordField />
                            </Box>
                            {/* <Box>
                                <Typography variant="subtitle2" color="textSecondary">Logged In</Typography>
                                <BooleanField source="logged_in" />
                            </Box> */}
                        </Stack>
                    </Box>

                    {/* Right column */}
                    <Box flex={1}>
                        <Stack spacing={3}>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Failed Login Attempts</Typography>
                                <TextField source="failed_login_attempts" />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Status</Typography>
                                <FunctionField
                                    render={record => <StatusField record={record} />}
                                />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Created At</Typography>
                                <DateField source="created_at" showTime />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Updated At</Typography>
                                <DateField source="updated_at" showTime />
                            </Box>
                            <Box>
                                <Typography variant="subtitle2" color="textSecondary">Deleted At</Typography>
                                <DateField source="deleted_at" showTime />
                            </Box>
                        </Stack>
                    </Box>
                </Box>
            </Paper>
        </SimpleShowLayout>
    </Show>
        
);

export const UserEdit = () => (
    <Edit>
        <SimpleForm>
        <Typography variant="h6">Account Info</Typography>
                        <TextInput source="username" label="Username" fullWidth />
                        <TextInput source="email" label="Email" type="email" fullWidth />
                        <SelectInput
                            source="role"
                            label="Role"
                            choices={[
                                { id: 'ROLE_PROVIDER', name: 'Provider' },
                                { id: 'ROLE_ADMIN', name: 'Admin' },
                            ]}
                            fullWidth
                        />
                        <PasswordInput source="password" label="Password" />
                        <SelectInput
                            source="status"
                            label="Status"
                            choices={[
                                { id: 1, name: 'Active' },
                                { id: 0, name: 'Inactive' },
                            ]}
                            fullWidth
                        />
        </SimpleForm>
    </Edit>
);